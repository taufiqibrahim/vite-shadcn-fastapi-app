import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlmodel import Session, create_engine, text
from sqlmodel.pool import StaticPool

from alembic.command import upgrade
from alembic.config import Config
from src.accounts.models import Account, AccountType
from src.accounts.schemas import AccountCreate
from src.auth.services.jwt import create_access_token, create_refresh_token
from src.auth.services.security import get_password_hash
from src.core.logging import get_logger, setup_logging
from src.database.session import get_db
from src.main import app

# Ensure the src directory is in the import path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, src_path)

setup_logging()
logger = get_logger(__name__)

TEST_ACCOUNT_UID = "e7a0a0fc-4f38-43ec-8e90-c0acb1774603"
TEST_ACCOUNT_EMAIL = "demo@example.com"
TEST_ACCOUNT_PASSWORD = "Password123"
TEST_SERVICE_ACCOUNT_EMAIL = "service@example.com"
TEST_SERVICE_ACCOUNT_PASSWORD = "service_password"

POSTGRES_SQLALCHEMY_URI = "postgresql://app:changeme123@localhost:5432/postgres"
TESTDB_SQLALCHEMY_URI = "postgresql://app:changeme123@localhost:5432/testdb"


def run_alembic_migration():
    from alembic.command import upgrade
    from alembic.config import Config

    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", TESTDB_SQLALCHEMY_URI)
    upgrade(alembic_config, "head")

    # Rerun setup_logging due to alembic logging is interfere with the app logging
    setup_logging()


# Create a clean DB schema for tests
@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    logger.info("Create testdb")
    with create_engine(
        POSTGRES_SQLALCHEMY_URI, isolation_level="AUTOCOMMIT"
    ).connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS testdb WITH (FORCE)"))
        conn.execute(text("CREATE DATABASE testdb"))

    logger.info("Create postgis extension")
    with create_engine(
        TESTDB_SQLALCHEMY_URI, isolation_level="AUTOCOMMIT"
    ).connect() as conn:
        conn.execute(text("CREATE EXTENSION postgis"))

    logger.info("Run alembic migrations")
    run_alembic_migration()


@pytest.fixture(scope="session")
def session_db():
    engine = create_engine(
        TESTDB_SQLALCHEMY_URI,
        isolation_level="AUTOCOMMIT",
        connect_args={},
        poolclass=StaticPool,
    )
    with Session(engine) as session:
        yield session


# Provide a fresh DB session per test
@pytest.fixture()
def db():
    # Set up
    engine = create_engine(
        TESTDB_SQLALCHEMY_URI,
        isolation_level="AUTOCOMMIT",
        connect_args={},
        poolclass=StaticPool,
    )
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


# ********* EMAIL FIXTURES ********************************************************************
@pytest.fixture
def mock_send_email(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr("src.utils.send_email_smtp", mock)
    return mock


# ********* TEST ACCOUNT FIXTURES ********************************************************************
@pytest.fixture(scope="session")
def test_account() -> AccountCreate:
    return AccountCreate(
        uid=TEST_ACCOUNT_UID,
        email=TEST_ACCOUNT_EMAIL,
        password=SecretStr(TEST_ACCOUNT_PASSWORD),
        full_name="Test User",
    )


@pytest.fixture(scope="session", autouse=True)
def test_account_db(session_db, test_account) -> Account:
    account = Account(
        email=test_account.email,
        hashed_password=get_password_hash(test_account.password),
        account_type=AccountType.USER,
    )
    session_db.add(account)
    session_db.commit()
    session_db.refresh(account)
    return account


@pytest.fixture
def test_account_access_token(test_account_db):
    data = {
        "sub": test_account_db.email,
        "id": test_account_db.id,
    }

    # Create token with custom expiration
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    return token


@pytest.fixture
def test_account_refresh_token(test_account_db):
    data = {
        "sub": test_account_db.email,
        "id": test_account_db.id,
    }

    # Create token with custom expiration
    token = create_refresh_token(data)
    return token


@pytest.fixture
def test_account_authorized_headers(test_account_access_token):
    return {"Authorization": f"Bearer {test_account_access_token}"}


# ********* TEST RANDOM ACCOUNT FIXTURES ********************************************************************
@pytest.fixture()
def test_random_account() -> AccountCreate:
    uid = uuid.uuid4()
    return AccountCreate(
        uid=uid,
        email=f"test_{str(uid).replace('-', '_')}@example.com",
        password=SecretStr(TEST_ACCOUNT_PASSWORD),
        full_name=f"test_{str(uid).replace('-', '_')}",
    )


@pytest.fixture()
def test_random_account_db(session_db, test_random_account) -> Account:
    account = Account(
        email=test_random_account.email,
        hashed_password=get_password_hash(test_random_account.password),
        account_type=AccountType.USER,
    )
    session_db.add(account)
    session_db.commit()
    session_db.refresh(account)
    return account


@pytest.fixture
def test_random_account_access_token(test_random_account_db):
    data = {
        "sub": test_random_account_db.email,
        "id": test_random_account_db.id,
    }

    # Create token with custom expiration
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    return token


@pytest.fixture
def test_random_account_refresh_token(test_random_account_db):
    data = {
        "sub": test_random_account_db.email,
        "id": test_random_account_db.id,
    }

    # Create token with custom expiration
    token = create_refresh_token(data)
    return token


@pytest.fixture
def test_random_account_authorized_headers(test_random_account_access_token):
    return {"Authorization": f"Bearer {test_random_account_access_token}"}
