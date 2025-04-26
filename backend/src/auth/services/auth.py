"""Core authentication logic"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.models import Account
from src.accounts.services import get_account_by_email
from src.auth.schemas import Token
from src.auth.services.jwt import create_access_token
from src.auth.services.security import verify_password
from src.core.exceptions import AccountDisabledException
from src.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[Account]:
    logger.debug("authenticate_user")
    user_account = await get_account_by_email(db, email=email)
    if not user_account:
        return None
    if not verify_password(password, user_account.hashed_password):
        return None
    return user_account


async def login_user(db: AsyncSession, email: str, password: str) -> Token:
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
