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
    db_account = Account(
        email=disabled_account.email,
        hashed_password=get_password_hash(disabled_account.password),
        disabled=True,
        account_type=AccountType.USER,
    )
    db.add(db_account)
    db.commit()

    response = client.post(
        "/api/v1/auth/login",
        data={"username": disabled_account.email, "password": disabled_account.password},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
