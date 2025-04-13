import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from src.auth.services import get_password_hash
from src.auth.schemas import Token
from src.auth.models import Account, AccountType


@pytest.fixture
def user(db: Session) -> Account:
    db.exec(delete(Account).where(Account.email == "testuser@example.com"))
    user = Account(
        email="testuser@example.com", hashed_password=get_password_hash("password"), account_type=AccountType.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def service_account(db: Session) -> Account:
    email = "testmachine@example.com"
    db.exec(delete(Account).where(Account.email == email))
    user = Account(email=email, hashed_password=get_password_hash("password"), account_type=AccountType.SERVICE_ACCOUNT)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_user_login(client: TestClient, db: Session, user: Account):
    """
    Test regular login success and failure cases
    """
    # Correct login
    response = client.post("/api/v1/auth/login", data={"username": user.email, "password": "password"})
    assert response.status_code == status.HTTP_200_OK
    token = Token.model_validate(response.json())
    assert token.access_token
    assert token.token_type == "bearer"

    # Wrong password
    response = client.post("/api/v1/auth/login", data={"username": user.email, "password": "wrong_password"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Wrong username
    response = client.post("/api/v1/auth/login", data={"username": "wrong@example.com", "password": "password"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_service_account_login_rejected(client: TestClient, service_account: Account):
    """
    Test that service-account type cannot login with bearer token
    """
    response = client.post("/api/v1/auth/login", data={"username": service_account.email, "password": "password"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_get_api_key_success_and_failure(client: TestClient, db: Session, service_account: Account, user: Account):
#     """
#     Get API key for machine account
#     Fail when regular user requests API key
#     """
#     # Login as machine user
#     response = client.post("/api/v1/auth/login", data={
#         "username": service_account.email,
#         "password": "password"
#     })
#     print(service_account.email, response.json(), response.status_code)
#     assert response.status_code == status.HTTP_200_OK
#     token = Token.model_validate(response.json())
