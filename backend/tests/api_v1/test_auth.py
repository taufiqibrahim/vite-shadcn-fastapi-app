import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from src.auth.services import get_password_hash
from src.auth.schemas import Token
from src.auth.models import Account, AccountType
from src.core.config import secret_settings


@pytest.fixture
def service_account(db: Session) -> Account:
    email = "testmachine@example.com"
    db.exec(delete(Account).where(Account.email == email))
    user = Account(email=email, hashed_password=get_password_hash("password"), account_type=AccountType.SERVICE_ACCOUNT)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_user_login(client: TestClient, test_account: Account):
    """
    Test regular login success and failure cases
    """
    # Correct login
    login_response = client.post(
        "/api/v1/auth/login", data={"username": test_account.email, "password": test_account.password}
    )
    print(login_response.json())
    assert login_response.status_code == status.HTTP_200_OK
    token = Token.model_validate(login_response.json())
    assert token.access_token
    assert token.token_type == "bearer"

    # Wrong password
    response = client.post("/api/v1/auth/login", data={"username": test_account.email, "password": "wrong_password"})
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
