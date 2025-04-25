from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlmodel import Session

from src.auth.models import Account
from src.auth.schemas import PasswordResetRequest
from src.auth.services.account import create_password_reset_token, get_account, get_account_by_email
from src.auth.services.auth import get_current_active_account
from src.auth.services.email import send_password_reset_email
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
async def get_self_account(
    payload: PasswordResetRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    email = payload.email
    account = await get_account_by_email(db=db, email=email)
    if not account:
        return

    password_reset_token = create_password_reset_token(db=db, account_id=account.id)
    background_tasks.add_task(send_password_reset_email, account.email, password_reset_token=password_reset_token)
