import asyncio
from typing import Optional

from fastapi import Depends, Header, Request
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError
from sqlmodel import Session
from temporalio.client import Client as TemporalClient

from src.accounts.models import Account
from src.accounts.services import get_account_by_api_key, get_account_by_email
from src.auth.schemas import TokenPayload
from src.auth.services.jwt import verify_access_token
from src.core.config import settings
from src.core.database import get_db
from src.core.exceptions import (
    AccountDisabledException,
    CredentialsValidationFailureException,
)
from src.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


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
            raise CredentialsValidationFailureException
        email: str = payload.sub
        if email is None:
            raise CredentialsValidationFailureException
    except JWTError:
        raise CredentialsValidationFailureException

    # Retrieve account by email
    account = get_account_by_email(db=db, email=email)
    if account is None:
        logger.debug("get_current_account_with_token: account is None")
        raise CredentialsValidationFailureException

    return account


async def get_current_account_with_api_key(x_api_key: str, db: Session):
    logger.debug("get_current_account_with_api_key")
    if settings.ENABLE_SERVICE_ACCOUNT_AUTH and x_api_key:
        account = await get_account_by_api_key(db=db, api_key=x_api_key)

        # if not account or account.account_type != models.AccountType.SERVICE_ACCOUNT:
        #     raise HTTPException(status_code=403, detail="Invalid or unauthorized API key")
        if account is None:
            raise CredentialsValidationFailureException
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
        return await get_current_account_with_api_key(x_api_key, db)
    else:
        raise CredentialsValidationFailureException


async def get_current_active_account(
    current_account: Account = Depends(get_current_account),
) -> Account:
    logger.debug("get_current_active_account")
    current_active_account = await current_account
    if current_active_account.disabled:
        raise AccountDisabledException
    return current_active_account


class TemporalClientProvider:
    def __init__(self):
        self._client: TemporalClient | None = None
        self._lock = asyncio.Lock()

    async def get(self) -> TemporalClient:
        async with self._lock:
            if not self._client:
                self._client = await TemporalClient.connect(settings.TEMPORAL_ADDRESS)
            return self._client


temporal_client_provider = TemporalClientProvider()


async def get_temporal_client() -> TemporalClient:
    return await temporal_client_provider.get()
