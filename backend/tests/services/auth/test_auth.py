import pytest
from datetime import timedelta
from sqlmodel import select
from src.auth.services import (
    verify_password,
    get_password_hash,
    create_api_key,
    create_access_token,
    decode_jwt,
)
from src.auth.models import Account, AccountType, APIKey
import uuid
import jwt


@pytest.mark.asyncio
async def test_password_hashing_and_verification():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    
    # Verify the password
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


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
    db_api_key = db.exec(
        select(APIKey).where(APIKey.key == api_key)
    ).first()
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
    decoded = decode_jwt(token)
    assert decoded.email == data["sub"]
    assert decoded.account_id == data["id"]


@pytest.mark.asyncio
async def test_create_access_token_default_expiration():
    """Test JWT token creation with default expiration"""
    data = {
        "sub": f"test_{uuid.uuid4()}@example.com",
        "id": 1,
    }
    
    token = create_access_token(data)
    decoded = decode_jwt(token)
    assert decoded.email == data["sub"]
    assert decoded.account_id == data["id"]


@pytest.mark.asyncio
async def test_decode_jwt_invalid_token():
    """Test JWT decoding with invalid token"""
    # Create a properly formatted JWT token with a valid base64 signature that will fail validation
    # This token has a valid format but uses a different secret key
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiaWQiOjEsImV4cCI6MTYxNjIzOTAyMn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    with pytest.raises(jwt.InvalidSignatureError):
        decode_jwt(invalid_token)


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
    db_api_key = db.exec(
        select(APIKey).where(APIKey.key == custom_key)
    ).first()
    assert db_api_key is not None
    assert db_api_key.account_id == account.id 