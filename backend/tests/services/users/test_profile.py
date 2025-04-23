import uuid

import pytest

from src.users.schemas import AccountCreate, UserProfileCreate
from src.users.services import create_user_account, create_user_profile


@pytest.mark.asyncio
async def test_create_user_profile_success(db):
    """Test creating a user profile"""
    # Create an account first with unique email
    unique_email = f"test_{uuid.uuid4()}@example.com"
    account_data = AccountCreate(email=unique_email, password="password123", full_name="Test User", account_type="user")
    account = create_user_account(db, account_data)

    # Create profile
    profile_data = UserProfileCreate(account_id=account.id, full_name="Test Profile")
    profile = create_user_profile(db, account.id, profile_data)

    assert profile is not None
    assert profile.full_name == profile_data.full_name
    assert profile.account_id == account.id
    assert profile.uid is not None


@pytest.mark.asyncio
async def test_create_user_profile_duplicate(db):
    """Test creating duplicate user profile"""
    # Create an account first with unique email
    unique_email = f"test_{uuid.uuid4()}@example.com"
    account_data = AccountCreate(email=unique_email, password="password123", full_name="Test User", account_type="user")
    account = create_user_account(db, account_data)

    # Create first profile
    profile_data = UserProfileCreate(account_id=account.id, full_name="Test Profile")
    profile1 = create_user_profile(db, account.id, profile_data)

    # Try to create another profile for the same account
    with pytest.raises(Exception):  # Should raise an integrity error
        create_user_profile(db, account.id, profile_data)
