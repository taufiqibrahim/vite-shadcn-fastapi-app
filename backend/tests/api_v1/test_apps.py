import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from src.apps.schemas import AppCreate
from src.users.schemas import AccountCreate, UserAccount


@pytest.fixture
def create_upload_user() -> AccountCreate:
    return AccountCreate(email="adminuser@example.com", password="password", full_name="Admin User")

@pytest.fixture
def create_app() -> AppCreate:
    return AppCreate(name="test-app", description="A test app")


def test_create_and_list_app(client: TestClient, create_app: AppCreate, create_upload_user: AccountCreate):
    """
    Test the POST /api/v1/apps/ endpoint.
    """
    print("new_user:", create_upload_user)
    response = client.post("/api/v1/users/", json=create_upload_user.model_dump())
    print("response", response.json())
    assert response.status_code == status.HTTP_201_CREATED
    created_user = UserAccount.model_validate(response.json())
    assert created_user.account_type == "user"

    # Log in to get a token
    login_response = client.post(
        "/api/v1/auth/login", data={"username": create_upload_user.email, "password": create_upload_user.password}
    )
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    print("token", token)

    print("new_app:", create_app)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/apps/", json=create_app.model_dump(), headers=headers)
    print("response", response.json())
    assert response.status_code == status.HTTP_201_CREATED

    # get all apps
    response = client.get("/api/v1/apps/", headers=headers)
    print(response.status_code)
    assert response.status_code == status.HTTP_200_OK
