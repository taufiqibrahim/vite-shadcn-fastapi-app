"""Core authentication logic"""

from src.auth.schemas import Token, TokenPayload
from src.core.logging import setup_logging, get_logger
from src.database.session import get_db

setup_logging()
logger = get_logger(__name__)

from typing import Optional

from fastapi import Depends, HTTPException, Header, Request, status
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session

from src.auth.services.account import get_account_by_api_key, get_account_by_email
from src.core.config import settings
from src.auth.models import Account
from src.auth.services.security import verify_password
from src.auth.exceptions import AccountDisabledException
from src.auth.services.jwt import create_access_token, verify_access_token

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[Account]:
    """
    Authenticate a user.

    Args:
        db: Database session
        email: User email
        password: User password

    Returns:
        Optional[User]: Authenticated user if successful, None otherwise
    """
    logger.debug("authenticate_user")
    user_account = await get_account_by_email(db, email=email)
    if not user_account:
        return None
    if not verify_password(password, user_account.hashed_password):
        return None
    return user_account


async def login_user(db: AsyncSession, email: str, password: str) -> Token:
    """
    Login a user and return an access token.

    Args:
        db: Database session
        credentials: User login credentials

    Returns:
        Token: Access token

    Raises:
        HTTPException: If authentication fails
    """
    logger.debug("login_user")
    user_account = await authenticate_user(db, email, password)
    if not user_account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user_account.disabled:
        raise AccountDisabledException
    return create_access_token(user_account)


async def get_optional_token(request: Request) -> Optional[str]:
    logger.debug("get_optional_token")
    auth = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(auth)
    if scheme.lower() == "bearer":
        return token
    return None


async def get_current_account_with_token(token: str, db: Session) -> Account:
    logger.debug("get_current_account_with_token")
    try:
        # Decode and validate the token (both signature and expiration)
        payload: TokenPayload = verify_access_token(token)
        if payload is None:
            raise credentials_exception
        email: str = payload.sub
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Retrieve account by email
    account = get_account_by_email(db=db, email=email)
    if account is None:
        raise credentials_exception

    return account


async def get_current_account_with_api_key(x_api_key: str, db: Session):
    logger.debug("get_current_account_with_api_key")
    if settings.ENABLE_SERVICE_ACCOUNT_AUTH and x_api_key:
        account = await get_account_by_api_key(db=db, api_key=x_api_key)

        # if not account or account.account_type != models.AccountType.SERVICE_ACCOUNT:
        #     raise HTTPException(status_code=403, detail="Invalid or unauthorized API key")
        if account is None:
            raise credentials_exception
        return account
    else:
        raise NotImplementedError("ENABLE_SERVICE_ACCOUNT_AUTH disabled")


async def get_current_account(
    token: Optional[str] = Depends(get_optional_token),
    x_api_key: Optional[str] = Header(default=None, alias=settings.API_KEY_HEADER),
    db: Session = Depends(get_db),
) -> Account:
    logger.debug("get_current_account")

    if token:
        return await get_current_account_with_token(token, db)
    elif x_api_key:
        return get_current_account_with_api_key(x_api_key, db)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_account(current_account: Account = Depends(get_current_account)) -> Account:
    logger.debug(f"get_current_active_account")
    if current_account.disabled:
        raise HTTPException(status_code=400, detail="Inactive account")
    return current_account


async def get_current_active_account_or_400(
    current_account: Optional[Account] = Depends(get_current_active_account),
    # account_by_api_key: Optional[models.Account] = Depends(get_account_by_api_key),
) -> Account:
    logger.debug(f"get_current_active_account_or_400")
    # account = current_account or account_by_api_key
    account = current_account
    if not account:
        raise HTTPException(status_code=400, detail="Authentication credentials were not provided")
    if account.disabled:
        raise HTTPException(status_code=400, detail="Inactive account")

    return account
