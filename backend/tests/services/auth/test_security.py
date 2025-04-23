import pytest

from src.auth.services.security import get_password_hash, verify_password


@pytest.mark.asyncio
async def test_password_hashing_and_verification():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed_password = get_password_hash(password)

    # Verify the password
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False
