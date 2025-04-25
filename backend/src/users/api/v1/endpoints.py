from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.auth import models
from src.auth.services import (
    get_current_active_account,
)
from src.core.logging import get_logger
from src.database.session import get_db
from src.users import schemas, services
from src.users.models import UserProfile

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/me", response_model=schemas.UserProfile)
async def read_users_me(
    current_account: models.Account = Depends(get_current_active_account), db: Session = Depends(get_db)
):
    logger.debug(f"read_users_me current_account={current_account}")
    if current_account.account_type != models.AccountType.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This endpoint is for human users only.",
        )

    profile = db.exec(select(UserProfile).where(UserProfile.account_id == current_account.id)).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


@router.post("/", response_model=schemas.UserAccount, status_code=status.HTTP_201_CREATED)
async def create_user(account: schemas.AccountCreate, db: Session = Depends(get_db)):

    db_account = services.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_account = services.create_user_account(db=db, account=account)
    profile = schemas.UserProfileCreate(account_id=created_account.id, full_name=account.full_name)
    services.create_user_profile(db, created_account.id, profile)

    return created_account


@router.get("/", response_model=List[schemas.UserAccount])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_account: models.Account = Depends(get_current_active_account),
):
    accounts = services.get_accounts(db, skip=skip, limit=limit)
    return accounts


@router.get("/{account_id}", response_model=schemas.UserAccount)
async def read_user(
    account_id: int,
    db: Session = Depends(get_db),
    current_account: models.Account = Depends(get_current_active_account),
):
    db_account = services.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account


@router.get("/me/api-key", response_model=str)
async def get_my_api_key(
    current_account: models.Account = Depends(get_current_active_account),
    db: Session = Depends(get_db),
):
    """
    Retrieves the API key for the current account.
    """
    if current_account.account_type != models.AccountType.SERVICE_ACCOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account is not a service account.",
        )
    #  Check if the account already has an API key.  For simplicity, we
    #  create a new one if it doesn't exist.  In a real application, you
    #  might want to handle this differently (e.g., return the existing key).
    api_key = db.exec(
        select(models.APIKey).where(
            models.APIKey.account_id == current_account.id,
            models.APIKey.is_active,
        )
    ).first()
    if api_key is None:
        key = services.create_api_key(db, current_account.id)
        return key
    return api_key.key
