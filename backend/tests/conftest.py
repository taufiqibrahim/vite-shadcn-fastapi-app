import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Ensure the src directory is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.main import app
from src.auth.models import Account
from src.database.session import get_db


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


# Optionally create a test user
@pytest.fixture()
def test_user(db: Session):
    user = Account(email="test@example.com", hashed_password="password", account_type="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
