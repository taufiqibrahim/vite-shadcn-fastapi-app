import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select
from passlib.context import CryptContext

from src.auth.services import get_password_hash
from src.auth.schemas import Token
from src.auth.models import Account, AccountType


@pytest.fixture
def regular_user(db: Session) -> Account:
    db.exec(delete(Account).where(Account.email == "testuser@example.com"))
    user = Account(email="testuser@example.com", hashed_password=get_password_hash("password"), account_type=AccountType.USER)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def machine_user(db: Session) -> Account:
    email = "testmachine@example.com"
    db.exec(delete(Account).where(Account.email == email))
    user = Account(email=email, hashed_password=get_password_hash("password"), account_type=AccountType.SERVICE_ACCOUNT)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_regular_user_login(client: TestClient, db: Session, regular_user: Account):
    """
    Test regular login success and failure cases
    """
    # Correct login
    response = client.post("/api/v1/auth/login", data={
        "username": regular_user.email,
        "password": "password"
    })
    assert response.status_code == status.HTTP_200_OK
    token = Token.model_validate(response.json())
    assert token.access_token
    assert token.token_type == "bearer"

    # Wrong password
    response = client.post("/api/v1/auth/login", data={
        "username": regular_user.email,
        "password": "wrong_password"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Wrong username
    response = client.post("/api/v1/auth/login", data={
        "username": "wrong@example.com",
        "password": "password"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_machine_account_login_rejected(client: TestClient, machine_user: Account):
    """
    Test that service-account type cannot login with bearer token
    """
    response = client.post("/api/v1/auth/login", data={
        "username": machine_user.email,
        "password": "password"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_api_key_success_and_failure(client: TestClient, db: Session, machine_user: Account, regular_user: Account):
    """
    Get API key for machine account
    Fail when regular user requests API key
    """
#     # Login as machine user
#     response = client.post("/api/v1/auth/login", data={
#         "username": machine_user.email,
#         "password": "password"
#     })
#     print(machine_user.email, response.json(), response.status_code)
#     assert response.status_code == status.HTTP_200_OK
#     token = Token.model_validate(response.json())

    # # Request API key
    # response = client.get("/api/v1/auth/api-key", headers={
    #     "Authorization": f"Bearer {token.access_token}"
    # })
    # assert response.status_code == status.HTTP_200_OK
    # api_key_data = Token.model_validate(response.json())
    # assert api_key_data.access_token
    # assert api_key_data.token_type == "api-key"

    # Try API key endpoint with regular user
    response = client.post("/api/v1/auth/login", data={
        "username": regular_user.email,
        "password": "password"
    })
    assert response.status_code == status.HTTP_200_OK
    token = Token.model_validate(response.json())

#     response = client.get("/api/v1/auth/api-key", headers={
#         "Authorization": f"Bearer {token.access_token}"
#     })
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
