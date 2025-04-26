from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, status
from sqlmodel import Session

from src.auth.models import Account
from src.auth.schemas import AccountUpdate, Token
from src.auth.services.account import get_account, get_account_by_email, update_account
from src.auth.services.auth import get_current_active_account
from src.auth.services.email import send_password_reset_email
from src.auth.services.jwt import create_access_token, create_refresh_token
from src.core.config import settings
from src.core.logging import get_logger, setup_logging
from src.database.session import get_db

setup_logging()
logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/accounts", tags=["Account"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_self_account(
    db: Session = Depends(get_db), current_account: Account = Depends(get_current_active_account)
):
    return await get_account(db=db, account_id=current_account.id)


@router.post("/password-reset", status_code=status.HTTP_201_CREATED)
async def create_password_reset(
    email: Annotated[str, Form()], background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    account = await get_account_by_email(db=db, email=email)
    if not account:
        return

    # Issue JWT access tokens as reset token with a small time window
    data = {"sub": account.email.lower(), "id": account.id}
    password_reset_token_expires = timedelta(minutes=settings.RESET_TOKEN_EXPIRY_MINUTES)
    password_reset_token = create_access_token(data=data, expires_delta=password_reset_token_expires)
    logger.debug(f"password_reset_token={password_reset_token}")
    background_tasks.add_task(send_password_reset_email, account.email, password_reset_token=password_reset_token)


@router.post("/confirm-password-reset", status_code=status.HTTP_200_OK)
async def confirm_password_reset(
    password: Annotated[str, Form()],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
):
    if not account.email or not account.hashed_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:

        account = await update_account(db=db, account=AccountUpdate(id=account.id, password=password))
        if account:
            # TODO:background_tasks.add_task(send_password_reset_succeed_email, account.email)

            # Issue JWT access + refresh tokens
            data = {"sub": account.email.lower(), "id": account.id}
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data=data, expires_delta=access_token_expires)
            refresh_token = create_refresh_token(data=data)

            return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
