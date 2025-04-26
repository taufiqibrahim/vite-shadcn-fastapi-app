from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.accounts.emails import (
    send_password_reset_email,
    send_password_reset_succeed_email,
    send_welcome_email,
)
from src.accounts.models import Account, AccountType
from src.accounts.schemas import AccountCreate, AccountUpdate
from src.accounts.services import (
    create_account,
    get_account,
    get_account_by_email,
    update_account,
)
from src.auth.schemas import Token, TokenRefresh
from src.auth.services.jwt import (
    create_access_token,
    create_refresh_token,
    get_refresh_token,
    refresh_access_token,
)
from src.auth.services.security import verify_password
from src.core.config import settings
from src.core.database import get_db
from src.core.exceptions import (
    AccountDisabledException,
    EmailAlreadyExistsException,
    InvalidLoginCredentialsException,
)
from src.core.logging import get_logger, setup_logging
from src.dependencies import get_current_active_account

setup_logging()
logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/accounts", tags=["Account"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Token)
async def signup(
    account: Annotated[AccountCreate, Form()],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):

    if not account.email or not account.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        account = await create_account(db=db, account=account)
        if account:
            background_tasks.add_task(send_welcome_email, account.email)

            # Issue JWT access + refresh tokens
            data = {"sub": account.email.lower(), "id": account.id}
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = create_access_token(
                data=data, expires_delta=access_token_expires
            )
            refresh_token = create_refresh_token(data=data)

            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )
    except EmailAlreadyExistsException:
        raise EmailAlreadyExistsException
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

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

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_self_account(
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_active_account),
):
    return await get_account(db=db, account_id=current_account.id)


@router.post("/refresh-token", response_model=TokenRefresh)
async def refresh_token(refresh_token: str = Depends(get_refresh_token)):
    """Endpoint to refresh the JWT access token using the refresh token"""
    new_access_token = refresh_access_token(refresh_token)
    return TokenRefresh(access_token=new_access_token, token_type="bearer")


@router.post("/reset-password", status_code=status.HTTP_201_CREATED)
async def create_password_reset(
    email: Annotated[str, Form()],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    account = await get_account_by_email(db=db, email=email)
    if not account:
        return

    # Issue JWT access tokens as reset token with a small time window
    data = {"sub": account.email.lower(), "id": account.id}
    password_reset_token_expires = timedelta(
        minutes=settings.RESET_TOKEN_EXPIRY_MINUTES
    )
    password_reset_token = create_access_token(
        data=data, expires_delta=password_reset_token_expires
    )
    logger.debug(f"password_reset_token={password_reset_token}")
    background_tasks.add_task(
        send_password_reset_email,
        account.email,
        password_reset_token=password_reset_token,
    )


@router.post("/confirm-reset-password", status_code=status.HTTP_200_OK)
async def confirm_password_reset(
    password: Annotated[str, Form()],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
):
    if not account.email or not account.hashed_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:

        account = await update_account(
            db=db, account=AccountUpdate(id=account.id, password=password)
        )
        if account:
            background_tasks.add_task(send_password_reset_succeed_email, account.email)

            # Issue JWT access + refresh tokens
            data = {"sub": account.email.lower(), "id": account.id}
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = create_access_token(
                data=data, expires_delta=access_token_expires
            )
            refresh_token = create_refresh_token(data=data)

            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
