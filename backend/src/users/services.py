import uuid

from sqlmodel import Session, select

from src.auth import models
from src.core.logging import get_logger, setup_logging
from src.users import schemas
from src.users.models import UserProfile

setup_logging()
logger = get_logger(__name__)


def get_account(db: Session, account_id: int):
    return db.exec(select(models.Account).where(models.Account.id == account_id)).first()


def get_account_by_email(db: Session, email: str):
    return db.exec(select(models.Account).where(models.Account.email == email)).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.exec(select(models.Account).offset(skip).limit(limit)).all()


# def create_user_account(db: Session, account: schemas.AccountCreate):
#     logger.debug(f"create_user_account")
#     hashed_password = get_password_hash(account.password) if account.password else None
#     db_account = models.Account(
#         email=account.email,
#         hashed_password=hashed_password,
#         disabled=account.disabled,
#         account_type=account.account_type,
#         uid=account.uid if account.uid else uuid.uuid4(),
#     )
#     db.add(db_account)
#     db.commit()
#     db.refresh(db_account)
#     return db_account


def create_user_profile(db: Session, account_id: int, profile: schemas.UserProfileCreate):
    db_profile = UserProfile(account_id=account_id, full_name=profile.full_name, uid=uuid.uuid4())  # Generate uid
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
