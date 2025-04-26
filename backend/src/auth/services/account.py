"""Account management service, database/model & logic"""

import secrets
import uuid
from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from src.auth.exceptions import EmailAlreadyExistsException
from src.auth.models import Account, APIKey
from src.auth.schemas import AccountCreate, AccountUpdate
from src.auth.services.security import get_password_hash
from src.core.logging import get_logger

logger = get_logger(__name__)


async def create_account(db: Session, account: AccountCreate) -> Account:
    """
    Create a new user account.

    Args:
        db: Database session
        account: Account creation data

    Returns:
        Account: The created account

    Raises:
        ValueError: If the email is already registered
    """
    logger.debug(f"Creating user account: {account.email}")

    # Check if email already exists
    existing_account = await get_account_by_email(db, account.email)
    if existing_account:
        raise EmailAlreadyExistsException

    # Create the account
    hashed_password = get_password_hash(account.password) if account.password else None
    db_account = Account(
        email=account.email.lower(),
        hashed_password=hashed_password,
        disabled=account.disabled,
        account_type=account.account_type,
        uid=account.uid if account.uid else uuid.uuid4(),
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    logger.debug(f"Created user account: {db_account.email.lower()}")

    return db_account


async def update_account(db: Session, account: AccountUpdate) -> Account:
    """
    Update an existing user account.
    """
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


async def get_account(db: Session, account_id: int) -> Optional[Account]:
    """
    Get an account by ID.

    Args:
        db: Database session
        account_id: ID of the account to retrieve

    Returns:
        Optional[Account]: The account if found, None otherwise
    """
    result = db.exec(select(Account).where(Account.id == account_id))
    return result.first()


async def get_account_by_email(db: Session, email: str) -> Optional[Account]:
    """
    Get an account by email.

    Args:
        db: Database session
        email: Email of the account to retrieve

    Returns:
        Optional[Account]: The account if found, None otherwise
    """
    result = db.exec(select(Account).where(Account.email == email.lower())).first()
    return result


async def get_account_by_api_key(db: Session, api_key: str) -> Optional[Account]:
    """
    Get an account by email.

    Args:
        db: Database session
        email: Email of the account to retrieve

    Returns:
        Optional[Account]: The account if found, None otherwise
    """
    result = db.exec(select(Account).join(APIKey).where(APIKey.key == api_key, APIKey.is_active)).first()
    return result


async def get_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[Account]:
    """
    Get a list of accounts with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List[Account]: List of accounts
    """
    result = db.exec(select(Account).offset(skip).limit(limit))
    return result.scalars().all()


def create_api_key(db: Session, account_id: int, level: int = 1, api_key: str = None) -> str:
    """
    Creates a new API key for the given account.
    """
    if not api_key or api_key is None:
        key = secrets.token_urlsafe(32)
    else:
        key = api_key
    db_api_key = APIKey(key=key, account_id=account_id, level=level)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return key
