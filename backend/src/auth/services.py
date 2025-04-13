from fastapi import Depends, HTTPException, status
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
from src.core.logging import logger
from src.database.session import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_settings.SECRET_KEY, algorithm=settings.JWT_ENCODE_ALGORITHM)


def decode_jwt_token(token: str) -> schemas.TokenData:
    try:
        payload = jwt.decode(token, secret_settings.SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALGORITHM])
        email: Optional[str] = payload.get("sub")
        account_id: Optional[int] = payload.get("id")
        if not email or not account_id:
            raise ValueError("Missing fields in token")
        return schemas.TokenData(email=email, account_id=account_id)
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_account(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.Account:
    logger.debug("get_current_account")
    token_data = decode_jwt_token(token)
    account = db.exec(select(models.Account).where(models.Account.email == token_data.email)).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account not found")
    return account


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


# async def get_current_account(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
# ):
#     logger.debug(f"get_current_account")
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, secret_settings.SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALGORITHM])
#         email: str = payload.get("sub")
#         account_id: int = payload.get("id")
#         logger.debug(f"get_current_account payload={payload}")
#         if email is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(email=email, account_id=account_id)
#         logger.debug(f"get_current_account token_data={token_data}")
#     except jwt.PyJWTError:
#         raise credentials_exception
#     account = (
#         db.exec(select(models.Account).where(models.Account.email == token_data.email)).first()
#     )
#     logger.debug(f"get_current_account account={account}")

#     if account is None:
#         raise credentials_exception
#     return account


# async def get_current_active_account(
#     current_account: models.Account = Depends(get_current_account)
# ):
#     logger.debug(f"get_current_active_account current_account={current_account}")
#     if current_account.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")

#     return current_account


# def create_api_key(db: Session, account_id: int, level: int = 1) -> str:
#     """
#     Creates a new API key for the given account.
#     """
#     key = secrets.token_urlsafe(32)  # Generate a secure random key
#     db_api_key = models.APIKey(key=key, account_id=account_id, level=level)
#     db.add(db_api_key)
#     db.commit()
#     db.refresh(db_api_key)
#     return key


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


# async def get_current_account_or_400(
#     current_account: models.Account = Depends(get_current_account),
#     account_by_api_key: Optional[models.Account] = Depends(get_account_by_api_key),
# ) -> models.Account:
#     """
#     Dependency that resolves the current account from either a session token
#     or an API key.  If both are provided, the session token takes precedence.
#     If neither is provided, it raises a 400 error.
#     """
#     if current_account:
#         return current_account
#     elif account_by_api_key:
#         return account_by_api_key
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Either a session token or an API key must be provided",
#         )


# async def get_current_active_account_or_400(
#     current_account: models.Account = Depends(get_current_active_account),
#     account_by_api_key: Optional[models.Account] = Depends(get_account_by_api_key),
# ) -> models.Account:
#     """
#     Dependency that resolves the current active account from either a session
#     token or an API key.  If both are provided, the session token takes
#     precedence.  If neither is provided, it raises a 400 error.
#     """
#     logger.debug("get_current_active_account_or_400")
#     account = await get_current_account_or_400(
#         current_account=current_account, account_by_api_key=account_by_api_key
#     )
#     logger.debug(f"get_current_active_account_or_400 current_account={current_account} account={account}")

#     if account.disabled:
#         raise HTTPException(status_code=400, detail="Inactive account")
#     return account
