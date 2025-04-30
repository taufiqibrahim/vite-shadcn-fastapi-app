import uuid
from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from src.accounts.models import Account, AccountProfile
from src.accounts.schemas import AccountCreate, AccountDelete, AccountProfileMe, AccountUpdate
from src.auth.services.security import get_password_hash
from src.core.exceptions import APINotImplementedError, EmailAlreadyExistsException
from src.core.logging import get_logger, setup_logging
from src.organizations.models import Organization
from src.projects.models import Project

setup_logging()
logger = get_logger(__name__)


async def create_account(db: Session, account: AccountCreate) -> Account:
    logger.debug(f"Creating user account: {account.email}")

    with db.begin():
        # Check if email already exists
        existing_account = await get_account_by_email(db, account.email)
        if existing_account:
            raise EmailAlreadyExistsException

        # Create the account
        hashed_password = (
            get_password_hash(account.password) if account.password else None
        )
        db_account = Account(
            email=account.email.lower(),
            hashed_password=hashed_password,
            disabled=account.disabled,
            account_type=account.account_type,
            uid=account.uid if account.uid else uuid.uuid4(),
        )

        db.add(db_account)

        # Create account profile
        db_account_profile = AccountProfile(
            account=db_account, full_name=account.full_name
        )
        db.add(db_account_profile)

        # Create default organization
        db_account_org = Organization(
            account=db_account, name="Default org", description="Default organization"
        )
        db.add(db_account_org)

        # Create default project
        db_account_project = Project(
            organization=db_account_org,
            name="Default project",
            description="Default project",
        )
        db.add(db_account_project)

        logger.debug(f"Created user account: {db_account.email.lower()}")

    return db_account


async def update_account(db: Session, account: AccountUpdate) -> Account:
    db_account = db.exec(select(Account).where(Account.id == account.id)).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    account_data = account.model_dump(exclude_unset=True)
    for key, value in account_data.items():
        if key == "password":
            db_account.hashed_password = get_password_hash(value)
        else:
            setattr(db_account, key, value)

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account


async def delete_account(db: Session, account: AccountDelete) -> Account:
    raise APINotImplementedError


async def get_account(db: Session, account_id: int) -> Optional[AccountProfileMe]:
    account, profile = db.exec(select(Account, AccountProfile).join(AccountProfile).where(Account.id == account_id)).first()
    return AccountProfileMe(
        uid=account.uid,
        email=account.email,
        disabled=account.disabled,
        full_name=profile.full_name,
        created_at=profile.created_at.isoformat(),
        updatedt_at=profile.updated_at.isoformat(),
    )


async def get_account_by_email(db: Session, email: str) -> Optional[Account]:
    result = db.exec(select(Account).where(Account.email == email.lower())).first()
    return result


# async def get_account_by_api_key(db: Session, api_key: str) -> Optional[Account]:
#     result = db.exec(
#         select(Account).join(APIKey).where(APIKey.key == api_key, APIKey.is_active)
#     ).first()
#     return result


async def get_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[Account]:
    result = db.exec(select(Account).offset(skip).limit(limit))
    return result.scalars().all()
