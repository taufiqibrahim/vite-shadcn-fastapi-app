from jose import JWTError
import pytest
import uuid
from fastapi import HTTPException
from datetime import timedelta
from sqlmodel import select

from src.auth.models import Account, AccountType, APIKey
from src.auth.services.account import create_api_key
from src.auth.services.auth import get_current_account_with_api_key, get_current_account_with_token
from src.auth.services.jwt import create_access_token, decode_and_validate_token
from src.auth.services.security import get_password_hash


@pytest.mark.asyncio
async def test_create_api_key(db):
    """Test API key creation"""
    # Create a test account
    account = Account(
        email=f"test_{uuid.uuid4()}@example.com",
        hashed_password=get_password_hash("password123"),
        account_type=AccountType.USER,
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    # Create API key
    api_key = create_api_key(db, account.id, level=1)

    # Verify the API key was created
    db_api_key = db.exec(select(APIKey).where(APIKey.key == api_key)).first()
    assert db_api_key is not None
    assert db_api_key.account_id == account.id
    assert db_api_key.level == 1
    assert db_api_key.is_active is True


@pytest.mark.asyncio
async def test_create_access_token():
    """Test JWT token creation and decoding"""
    # Create token data
    data = {
        "sub": f"test_{uuid.uuid4()}@example.com",
        "id": 1,
    }

    # Create token with custom expiration
    token = create_access_token(data, expires_delta=timedelta(minutes=15))

    # Decode and verify token
    decoded = decode_and_validate_token(token)
    assert decoded.sub == data["sub"]
    assert decoded.id == data["id"]


@pytest.mark.asyncio
async def test_create_access_token_default_expiration():
    """Test JWT token creation with default expiration"""
    data = {
        "sub": f"test_{uuid.uuid4()}@example.com",
        "id": 1,
    }

    token = create_access_token(data)
    decoded = decode_and_validate_token(token)
    assert decoded.sub == data["sub"]
    assert decoded.id == data["id"]


@pytest.mark.asyncio
async def test_decode_jwt_invalid_token():
    """Test JWT decoding with invalid token"""
    # Create a properly formatted JWT token with a valid base64 signature that will fail validation
    # This token has a valid format but uses a different secret key
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiaWQiOjEsImV4cCI6MTYxNjIzOTAyMn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    with pytest.raises(JWTError):
        decode_and_validate_token(invalid_token)


@pytest.mark.asyncio
async def test_create_api_key_with_custom_key(db):
    """Test API key creation with custom key"""
    # Create a test account
    account = Account(
        email=f"test_{uuid.uuid4()}@example.com",
        hashed_password=get_password_hash("password123"),
        account_type=AccountType.USER,
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    # Create API key with custom key
    custom_key = f"custom_api_key_{uuid.uuid4()}"
    api_key = create_api_key(db, account.id, level=1, api_key=custom_key)

    # Verify the API key was created with the custom key
    assert api_key == custom_key
    db_api_key = db.exec(select(APIKey).where(APIKey.key == custom_key)).first()
    assert db_api_key is not None
    assert db_api_key.account_id == account.id


@pytest.mark.asyncio
async def test_get_account_from_valid_token(session_db, test_account_db):
    """
    Test get_current_account_with_token
    """
    # Create token data
    data = {
        "sub": test_account_db.email,
        "id": test_account_db.id,
    }

    # Create token with custom expiration
    token = create_access_token(data, expires_delta=timedelta(minutes=15))

    account = await get_current_account_with_token(token, session_db)
    assert account is not None
    assert account.email == data["sub"]


@pytest.mark.asyncio
async def test_get_account_from_invalid_token(session_db):
    """
    Test test_get_account_from_invalid_token
    """
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vQGV4YW1wbGUuY29tIiwiaWQiOjEsImV4cCI6MTc0NTMxMzU0Nn0.cyDR0owt-T5RNhW10xyptN72hAf80sHxPypdxWXLias"
    with pytest.raises(HTTPException) as exc_info:
        await get_current_account_with_token(invalid_token, db=session_db)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_account_from_valid_api_key(session_db, test_account_db):
    """
    Test test_get_account_from_valid_api_key
    """
    # Create token with custom expiration
    api_key = create_api_key(db=session_db, account_id=test_account_db.id)

    account = await get_current_account_with_api_key(x_api_key=api_key, db=session_db)

    assert account is not None
    assert account.email == test_account_db.email


@pytest.mark.asyncio
async def test_get_account_from_invalid_api_key(session_db):
    """
    Test test_get_account_from_invalid_api_key
    """
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vQGV4YW1wbGUuY29tIiwiaWQiOjEsImV4cCI6MTc0NTMxMzU0Nn0.cyDR0owt-T5RNhW10xyptN72hAf80sHxPypdxWXLias"
    with pytest.raises(HTTPException) as exc_info:
        await get_current_account_with_api_key(invalid_token, db=session_db)

    assert exc_info.value.status_code == 401
