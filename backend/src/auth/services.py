from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
import jwt  # Import pyjwt
import secrets
from typing import Optional

from src.auth import schemas
from src.auth import models  # Import the Account and APIKey model
from src.core.config import settings
from src.database.session import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  #  Adjust the tokenUrl
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )  # Default expiration
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )  #  Use settings
    return encoded_jwt


async def get_current_account(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )  #  Use settings
        email: str = payload.get("sub")
        account_id: int = payload.get("id") # Get the account ID from the token
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, account_id=account_id) # Pass the account ID
    except JWTError:
        raise credentials_exception
    account = (
        db.exec(select(models.Account).where(models.Account.email == token_data.email)).first()
    )
    if account is None:
        raise credentials_exception
    return account


async def get_current_active_account(
    current_account: models.Account = Depends(get_current_account)
):
    if current_account.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_account


def create_api_key(db: Session, account_id: int, level: int = 1) -> str:
    """
    Creates a new API key for the given account.
    """
    key = secrets.token_urlsafe(32)  # Generate a secure random key
    db_api_key = models.APIKey(key=key, account_id=account_id, level=level)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return key


async def get_account_by_api_key(
    db: Session = Depends(get_db), api_key: str = Depends(api_key_header)
) -> Optional[models.Account]:
    """
    Retrieves an account based on the provided API key.
    """
    api_key_record = (
        db.exec(
            select(models.APIKey)
            .where(models.APIKey.key == api_key, models.APIKey.is_active == True)
        )
        .first()
    )
    if api_key_record:
        return api_key_record.account
    return None


async def get_current_account_by_api_key(
    account: Optional[models.Account] = Depends(get_account_by_api_key),
) -> models.Account:
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return account


async def get_current_account_or_400(
    current_account: models.Account = Depends(get_current_account),
    account_by_api_key: Optional[models.Account] = Depends(get_account_by_api_key),
) -> models.Account:
    """
    Dependency that resolves the current account from either a session token
    or an API key.  If both are provided, the session token takes precedence.
    If neither is provided, it raises a 400 error.
    """
    if current_account:
        return current_account
    elif account_by_api_key:
        return account_by_api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either a session token or an API key must be provided",
        )


async def get_current_active_account_or_400(
    current_account: models.Account = Depends(get_current_active_account),
    account_by_api_key: Optional[models.Account] = Depends(get_account_by_api_key),
) -> models.Account:
    """
    Dependency that resolves the current active account from either a session
    token or an API key.  If both are provided, the session token takes
    precedence.  If neither is provided, it raises a 400 error.
    """
    account = await get_current_account_or_400(
        current_account=current_account, account_by_api_key=account_by_api_key
    )
    if account.disabled:
        raise HTTPException(status_code=400, detail="Inactive account")
    return account
