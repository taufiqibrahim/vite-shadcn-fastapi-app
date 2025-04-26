from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.auth.exceptions import AccountDisabledException, EmailAlreadyExistsException, InvalidLoginCredentialsException
from src.auth.models import AccountType
from src.auth.schemas import AccountCreate, Token, TokenRefresh
from src.auth.services.account import create_account, get_account_by_email
from src.auth.services.email import send_welcome_email
from src.auth.services.jwt import create_access_token, create_refresh_token, get_refresh_token, refresh_access_token
from src.auth.services.security import verify_password
from src.core.config import settings
from src.core.logging import get_logger, setup_logging
from src.database.session import get_db

setup_logging()
logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Token)
async def signup(
    account: Annotated[AccountCreate, Form()], background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):

    if not account.email or not account.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        account = await create_account(db=db, account=account)
        if account:
            background_tasks.add_task(send_welcome_email, account.email)

            # Issue JWT access + refresh tokens
            data = {"sub": account.email.lower(), "id": account.id}
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data=data, expires_delta=access_token_expires)
            refresh_token = create_refresh_token(data=data)

            return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except EmailAlreadyExistsException:
        raise EmailAlreadyExistsException
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Lookup user by email in database
    account = await get_account_by_email(db=db, email=form_data.username.lower())
    if not account or account.account_type != AccountType.USER:
        logger.debug("not account or account.account_type")
        raise InvalidLoginCredentialsException

    # Verify password using hashing
    if not verify_password(form_data.password, account.hashed_password):
        logger.debug("not verify_password")
        raise InvalidLoginCredentialsException

    # Check if user is active / not disabled
    if account.disabled:
        logger.debug("account.disabled")
        raise AccountDisabledException

    # TODO: Create a session entry in the DB

    # Issue JWT access + refresh tokens
    data = {"sub": account.email.lower(), "id": account.id}
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=data, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data=data)

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh_token", response_model=TokenRefresh)
async def refresh_token(refresh_token: str = Depends(get_refresh_token)):
    """Endpoint to refresh the JWT access token using the refresh token"""
    new_access_token = refresh_access_token(refresh_token)
    return TokenRefresh(access_token=new_access_token, token_type="bearer")
