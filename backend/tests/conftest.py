import uuid
import jwt
from src.core.logging import setup_logging
from src.database.session import get_db
from src.main import app
import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from src.users.schemas import AccountCreate

# Ensure the src directory is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

setup_logging()


# Create an in-memory SQLite engine for isolated tests
@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)


# Create a clean DB schema for tests
@pytest.fixture(scope="session", autouse=True)
def prepare_database(engine):
    SQLModel.metadata.create_all(engine)


# Provide a fresh DB session per test
@pytest.fixture()
def db(engine):
    with Session(engine) as session:
        yield session


# Override the app DB dependency to use the test DB session
@pytest.fixture(autouse=True)
def override_get_db(db):
    def _get_test_db():
        yield db

    app.dependency_overrides[get_db] = _get_test_db


# Provide a FastAPI test client
@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def create_test_user() -> AccountCreate:
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    return AccountCreate(email=unique_email, password="password", full_name="Admin User")


@pytest.fixture
def auth_token(client: TestClient, create_test_user):
    # Create user
    response = client.post("/api/v1/users/", json=create_test_user.model_dump())
    assert response.status_code == 201

    # Log in user
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": create_test_user.email, "password": create_test_user.password},
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


@pytest.fixture
def authorized_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def authorized_account_id(auth_token):
    decoded = jwt.decode(auth_token, options={"verify_signature": False})
    return decoded["id"]


@pytest.fixture
def temporal_backend():
    return TemporalBackend()
