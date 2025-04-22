import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from src.auth.services import get_password_hash
from src.auth.schemas import Token
from src.auth.models import Account, AccountType, UserProfile
from src.users.schemas import AccountCreate, UserAccount


@pytest.fixture
def create_user() -> AccountCreate:
    return AccountCreate(
        email="newuser@example.com",
        password="password",
        full_name="New User",
    )


def test_regular_user_create_login_get_profile(client: TestClient, create_user: AccountCreate):
    """
    Test the POST /api/v1/users/ endpoint.
    """
    print("new_user:", create_user)
    response = client.post("/api/v1/users/", json=create_user.model_dump(mode="json"))
    print("response", response.json())
    assert response.status_code == status.HTTP_201_CREATED
    created_user = UserAccount.model_validate(response.json())
    assert created_user.account_type == "user"

    # Test with an existing email
    response = client.post("/api/v1/users/", json=create_user.model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Log in to get a token
    login_response = client.post(
        "/api/v1/auth/login", data={"username": create_user.email, "password": create_user.password}
    )
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    print("token", token)

    # Get the user's profile
    response = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    print(response.status_code, response.json())
    assert response.status_code == status.HTTP_200_OK
    profile = UserProfile.model_validate(response.json())
    assert profile.full_name == "New User"


# def test_read_users(client: TestClient, test_user: Account, db: Session):
#     """
#     Test the /users/ endpoint to get all users.
#     """
#     # Log in to get a token.  Need to log in as a user.
#     login_response = client.post(
#         "/auth/login", data={"username": "test@example.com", "password": "password"}
#     )
#     assert login_response.status_code == status.HTTP_200_OK
#     token = login_response.json()["access_token"]

#     response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == status.HTTP_200_OK
#     users = [Account.parse_obj(user) for user in response.json()]
#     assert len(users) >= 1
#     assert any(user.email == "test@example.com" for user in users)

# def test_read_user(client: TestClient, test_user: Account, db: Session):
#     """
#     Test the /users/{user_id} endpoint.
#     """
#     # Log in to get a token
#     login_response = client.post(
#         "/auth/login", data={"username": "test@example.com", "password": "password"}
#     )
#     assert login_response.status_code == status.HTTP_200_OK
#     token = login_response.json()["access_token"]

#     response = client.get(f"/users/{test_user.id}", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == status.HTTP_200_OK
#     user = Account.parse_obj(response.json())
#     assert user.email == "test@example.com"

#     # Test with a non-existent user ID
#     response = client.get("/users/9999", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == status.HTTP_404_NOT_FOUND

# def test_get_my_api_key(client: TestClient, db: Session):
#     """
#     Test the /users/me/api-key endpoint.
#     """
#     # Create a machine account
#     machine_user = Account(email="machine@example.com", hashed_password="password", account_type="service-account")
#     db.add(machine_user)
#     db.commit()
#     db.refresh(machine_user)

#     # Log in as the machine user to get a token
#     login_response = client.post(
#         "/auth/login", data={"username": "machine@example.com", "password": "password"}
#     )
#     assert login_response.status_code == status.HTTP_200_OK
#     token = login_response.json()["access_token"]

#     # Get the API key
#     response = client.get("/users/me/api-key", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == status.HTTP_200_OK
#     api_key = response.text
#     assert api_key is not None

#     # Test for a regular user, should fail
#     login_response = client.post(
#         "/auth/login", data={"username": "test@example.com", "password": "password"}
#     )
#     assert login_response.status_code == status.HTTP_200_OK
#     token = login_response.json()["access_token"]
#     response = client.get("/users/me/api-key", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == status.HTTP_400_BAD_REQUEST


# def test_get_account_by_key(client: TestClient, db: Session):
#     """
#     Test the /users/by-api-key/ endpoint.
#     """
#     # Create a machine account and get its API key
#     machine_user = Account(email="machine2@example.com", hashed_password="password", account_type="service-account")
#     db.add(machine_user)
#     db.commit()
#     db.refresh(machine_user)
#     api_key = services.create_api_key(db, machine_user.id)

#     # Call the endpoint to get the account by API key
#     response = client.get(f"/users/by-api-key/", headers={"X-API-Key": api_key})
#     assert response.status_code == status.HTTP_200_OK
#     account = Account.parse_obj(response.json())
#     assert account.email == "machine2@example.com"

#     # Test with an invalid API key
#     response = client.get("/users/by-api-key/", headers={"X-API-Key": "invalid_api_key"})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
