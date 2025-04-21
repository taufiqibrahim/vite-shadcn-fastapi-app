from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
import jwt
import secrets
from typing import Optional

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="passlib")

from src.auth import schemas
from src.auth import models
from src.core.config import settings, secret_settings
from src.core.logging import get_logger

logger = get_logger(__name__)
from src.database.session import get_db
from passlib.context import CryptContext


API_KEY_HEADER = "X-API-Key"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
api_key_header = APIKeyHeader(name=API_KEY_HEADER)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_api_key(db: Session, account_id: int, level: int = 1, api_key: str = None) -> str:
    """
    Creates a new API key for the given account.
    """
    if not api_key or api_key is None:
        key = secrets.token_urlsafe(32)  # Generate a secure random key
    else:
        key = api_key
    db_api_key = models.APIKey(key=key, account_id=account_id, level=level)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return key


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_settings.SECRET_KEY, algorithm=settings.JWT_ENCODE_ALGORITHM)


def decode_jwt(token: str) -> schemas.TokenData:
    payload = jwt.decode(token, secret_settings.SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALGORITHM])
    email: Optional[str] = payload.get("sub")
    account_id: Optional[int] = payload.get("id")
    if not email or not account_id:
        raise ValueError("Missing fields in token")
    return schemas.TokenData(email=email, account_id=account_id)


async def get_current_account(
    authorization: Optional[str] = Header(default=None),
    x_api_key: Optional[str] = Header(default=None, alias=API_KEY_HEADER),
    db: Session = Depends(get_db),
) -> models.Account:

    # TRY JWT
    if authorization:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid Authorization header")
        token = authorization.removeprefix("Bearer ").strip()
        try:
            token_data = decode_jwt(token)
            account = db.exec(select(models.Account).where(models.Account.email == token_data.email)).first()
            if not account:
                raise HTTPException(status_code=401, detail="Account not found")
            return account
        except (jwt.PyJWTError, ValueError):
            if not settings.ENABLE_SERVICE_ACCOUNT_AUTH:
                raise HTTPException(status_code=401, detail="Invalid token")

    # TRY API KEY ONLY IF ENABLED
    if settings.ENABLE_SERVICE_ACCOUNT_AUTH and x_api_key:
        account = db.exec(
            select(models.Account)
            .join(models.APIKey)
            .where(models.APIKey.key == x_api_key, models.APIKey.is_active == True)
        ).first()

        if not account or account.account_type != models.AccountType.SERVICE_ACCOUNT:
            raise HTTPException(status_code=403, detail="Invalid or unauthorized API key")

        return account

    raise HTTPException(status_code=401, detail="Authentication required")


async def get_account_by_api_key(
    api_key: str = Depends(api_key_header), db: Session = Depends(get_db)
) -> Optional[models.Account]:
    api_key_record = db.exec(
        select(models.APIKey).where(models.APIKey.key == api_key, models.APIKey.is_active == True)
    ).first()
    return api_key_record.account if api_key_record else None


async def get_current_active_account(current_account: models.Account = Depends(get_current_account)) -> models.Account:
    logger.debug(f"get_current_active_account")
    if current_account.disabled:
        raise HTTPException(status_code=400, detail="Inactive account")
    return current_account


async def get_current_account_or_400(
    current_account: Optional[models.Account] = Depends(get_current_account),
    account_by_api_key: Optional[models.Account] = Depends(get_account_by_api_key),
) -> models.Account:
    if current_account:
        return current_account
    if account_by_api_key:
        return account_by_api_key
    raise HTTPException(status_code=400, detail="Authentication credentials were not provided")


async def get_current_active_account_or_400(
    current_account: Optional[models.Account] = Depends(get_current_active_account),
    # account_by_api_key: Optional[models.Account] = Depends(get_account_by_api_key),
) -> models.Account:
    logger.debug("get_current_active_account_or_400")
    # account = current_account or account_by_api_key
    account = current_account
    if not account:
        raise HTTPException(status_code=400, detail="Authentication credentials were not provided")
    if account.disabled:
        raise HTTPException(status_code=400, detail="Inactive account")

    return account


# async def get_account_by_api_key(
#     db: Session = Depends(get_db), api_key: str = Depends(api_key_header)
# ) -> Optional[models.Account]:
#     """
#     Retrieves an account based on the provided API key.
#     """
#     api_key_record = (
#         db.exec(
#             select(models.APIKey)
#             .where(models.APIKey.key == api_key, models.APIKey.is_active == True)
#         )
#         .first()
#     )
#     if api_key_record:
#         return api_key_record.account
#     return None


# async def get_current_account_by_api_key(
#     account: Optional[models.Account] = Depends(get_account_by_api_key),
# ) -> models.Account:
#     if not account:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid API Key",
#         )
#     return account
