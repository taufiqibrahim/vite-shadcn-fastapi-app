import pytest
from fastapi import status
from src.auth.models import Account, AccountType
from src.auth.services import get_password_hash
from src.users.schemas import AccountCreate


@pytest.mark.asyncio
async def test_login_success(client, test_account):
    """Test successful login with correct credentials"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_account.email, "password": test_account.password},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_disabled_account(client, db):
    """Test login attempt with disabled account"""
    # Create a disabled account
    disabled_account = AccountCreate(
        email="disabled@example.com",
        password="password123",
        disabled=True,
        account_type=AccountType.USER,
    )
    hashed_password = get_password_hash(disabled_account.password)
    db_account = Account(
        email=disabled_account.email,
        hashed_password=hashed_password,
        disabled=True,
        account_type=AccountType.USER,
    )
    db.add(db_account)
    db.commit()

    response = client.post(
        "/api/v1/auth/login",
        data={"username": disabled_account.email, "password": disabled_account.password},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_current_user_success(client, test_account_authorized_headers):
    """Test getting current user with valid token"""
    response = client.get("/api/v1/auth/me", headers=test_account_authorized_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_account_authorized_headers.email


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user_no_token(client):
    """Test getting current user without token"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_api_key_success(client, test_account_authorized_headers):
    """Test creating a new API key"""
    response = client.post(
        "/api/v1/auth/api-keys",
        headers=test_account_authorized_headers,
        json={"level": 1},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "key" in data
    assert "level" in data
    assert data["level"] == 1


@pytest.mark.asyncio
async def test_list_api_keys_success(client, test_account_authorized_headers):
    """Test listing API keys"""
    response = client.get("/api/v1/auth/api-keys", headers=test_account_authorized_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_delete_api_key_success(client, test_account_authorized_headers, db):
    """Test deleting an API key"""
    # First create an API key
    create_response = client.post(
        "/api/v1/auth/api-keys",
        headers=test_account_authorized_headers,
        json={"level": 1},
    )
    api_key = create_response.json()["key"]

    # Then delete it
    response = client.delete(
        f"/api/v1/auth/api-keys/{api_key}",
        headers=test_account_authorized_headers,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify it's deleted
    verify_response = client.get("/api/v1/auth/api-keys", headers=test_account_authorized_headers)
    assert api_key not in [key["key"] for key in verify_response.json()]
