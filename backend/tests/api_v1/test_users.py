import pytest
from fastapi import status
from src.users.schemas import AccountCreate, UserProfileCreate


@pytest.mark.asyncio
async def test_create_user_success(client, db):
    """Test successful user creation"""
    user_data = AccountCreate(
        email="newuser@example.com", password="password123", full_name="New User", account_type="user"
    )

    response = client.post("/api/v1/users/", json=user_data.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data.email
    assert "id" in data
    assert "uid" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client, test_account):
    """Test user creation with duplicate email"""
    user_data = AccountCreate(
        email=test_account.email,  # Using existing email
        password="password123",
        full_name="Duplicate User",
        account_type="user",
    )

    response = client.post("/api/v1/users/", json=user_data.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_user_success(client, test_account_authorized_headers, test_account):
    """Test getting user details"""
    response = client.get("/api/v1/users/me", headers=test_account_authorized_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_account.email
    assert "id" in data
    assert "uid" in data


@pytest.mark.asyncio
async def test_update_user_success(client, test_account_authorized_headers):
    """Test updating user details"""
    update_data = {"full_name": "Updated Name", "email": "updated@example.com"}

    response = client.patch("/api/v1/users/me", headers=test_account_authorized_headers, json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["email"] == update_data["email"]


@pytest.mark.asyncio
async def test_create_user_profile_success(client, test_account_authorized_headers, test_account):
    """Test creating user profile"""
    profile_data = UserProfileCreate(full_name="Test User Profile")

    response = client.post(
        "/api/v1/users/me/profile", headers=test_account_authorized_headers, json=profile_data.model_dump()
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["full_name"] == profile_data.full_name
    assert "id" in data
    assert "uid" in data


@pytest.mark.asyncio
async def test_get_user_profile_success(client, test_account_authorized_headers):
    """Test getting user profile"""
    response = client.get("/api/v1/users/me/profile", headers=test_account_authorized_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "full_name" in data
    assert "id" in data
    assert "uid" in data


@pytest.mark.asyncio
async def test_update_user_profile_success(client, test_account_authorized_headers):
    """Test updating user profile"""
    update_data = {"full_name": "Updated Profile Name"}

    response = client.patch("/api/v1/users/me/profile", headers=test_account_authorized_headers, json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == update_data["full_name"]


@pytest.mark.asyncio
async def test_list_users_success(client, test_account_authorized_headers):
    """Test listing users"""
    response = client.get("/api/v1/users/", headers=test_account_authorized_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("email" in user for user in data)
    assert all("id" in user for user in data)
