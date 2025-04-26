import uuid

import pytest
from pydantic import SecretStr

from src.auth.models import AccountType
from src.users.schemas import AccountCreate
from src.users.services import (
    create_user_account,
    get_account,
    get_account_by_email,
    get_accounts,
)


@pytest.mark.asyncio
async def test_get_account_success(db):
    """Test getting account by ID"""
    # Create an account first with unique email
    unique_email = f"test_{uuid.uuid4()}@example.com"
    account_data = AccountCreate(
        email=unique_email,
        password=SecretStr("password123"),
        full_name="Test User",
        account_type="user",
    )
    account = create_user_account(db, account_data)

    # Test getting the account
    retrieved_account = get_account(db, account.id)
    assert retrieved_account is not None
    assert retrieved_account.email == unique_email
    assert retrieved_account.id == account.id


@pytest.mark.asyncio
async def test_get_account_not_found(db):
    """Test getting non-existent account"""
    account = get_account(db, 999999)  # Non-existent ID
    assert account is None


@pytest.mark.asyncio
async def test_get_account_by_email_success(db):
    """Test getting account by email"""
    # Create an account first with unique email
    unique_email = f"test_{uuid.uuid4()}@example.com"
    account_data = AccountCreate(
        email=unique_email,
        password=SecretStr("password123"),
        full_name="Test User",
        account_type="user",
    )
    account = create_user_account(db, account_data)

    # Test getting the account
    retrieved_account = get_account_by_email(db, unique_email)
    assert retrieved_account is not None
    assert retrieved_account.email == unique_email
    assert retrieved_account.id == account.id


@pytest.mark.asyncio
async def test_get_account_by_email_not_found(db):
    """Test getting account by non-existent email"""
    account = get_account_by_email(db, f"nonexistent_{uuid.uuid4()}@example.com")
    assert account is None


@pytest.mark.asyncio
async def test_get_accounts_success(db):
    """Test getting multiple accounts"""
    # Create multiple accounts with unique emails
    accounts = [
        AccountCreate(
            email=f"test_{uuid.uuid4()}@example.com",
            password=SecretStr("password123"),
            full_name=f"Test User {i}",
            account_type="user",
        )
        for i in range(3)
    ]

    for account_data in accounts:
        create_user_account(db, account_data)

    # Test getting accounts with pagination
    retrieved_accounts = get_accounts(db, skip=0, limit=10)
    assert len(retrieved_accounts) >= 3  # Could be more if test_account exists

    # Test pagination
    paginated_accounts = get_accounts(db, skip=1, limit=2)
    assert len(paginated_accounts) <= 2


@pytest.mark.asyncio
async def test_create_user_account_success(db):
    """Test creating a new user account"""
    account_data = AccountCreate(
        email=f"newuser_{uuid.uuid4()}@example.com",
        password=SecretStr("password123"),
        full_name="New User",
        account_type="user",
    )

    account = create_user_account(db, account_data)
    assert account is not None
    assert account.email == account_data.email
    assert account.hashed_password is not None
    assert account.account_type == AccountType.USER
    assert account.uid is not None
