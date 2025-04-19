import jwt
from src.auth.models import Account, AccountType
from src.auth.services import get_password_hash
from src.core.logging import setup_logging, get_logger
from src.database.session import get_db
from src.main import app
import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, text
from sqlmodel.pool import StaticPool
from src.users.schemas import AccountCreate

from alembic.command import upgrade
from alembic.config import Config

# Ensure the src directory is in the import path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, src_path)

setup_logging()
logger = get_logger(__name__)

TEST_ACCOUNT_UID = "e7a0a0fc-4f38-43ec-8e90-c0acb1774603"
TEST_ACCOUNT_EMAIL = "demo@example.com"
TEST_ACCOUNT_PASSWORD = "password"

POSTGRES_SQLALCHEMY_URI = "postgresql://app:changeme123@localhost:25432/postgres"
TESTDB_SQLALCHEMY_URI = "postgresql://app:changeme123@localhost:25432/testdb"


def run_alembic_migration():
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", TESTDB_SQLALCHEMY_URI)
    upgrade(alembic_config, "head")


def create_test_account():
    """Create demo user on preparation"""
    account_db = Account(
        uid=TEST_ACCOUNT_UID,
        email=TEST_ACCOUNT_EMAIL,
        hashed_password=get_password_hash(TEST_ACCOUNT_PASSWORD),
        account_type=AccountType.USER,
    )
    with Session(create_engine(TESTDB_SQLALCHEMY_URI, isolation_level="AUTOCOMMIT")) as session:
        session.add(account_db)
        session.commit()
        session.refresh(account_db)


# Create a clean DB schema for tests
@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    logger.info("Create testdb")
    with create_engine(POSTGRES_SQLALCHEMY_URI, isolation_level="AUTOCOMMIT").connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS testdb WITH (FORCE)"))
        conn.execute(text("CREATE DATABASE testdb"))

    logger.info("Create postgis extension")
    with create_engine(TESTDB_SQLALCHEMY_URI, isolation_level="AUTOCOMMIT").connect() as conn:
        conn.execute(text("CREATE EXTENSION postgis"))

    logger.info("Run alembic migrations")
    run_alembic_migration()

    create_test_account()


# Create an ephemeral Postgis engine for isolated tests
@pytest.fixture()
def engine():
    return create_engine(TESTDB_SQLALCHEMY_URI, isolation_level="AUTOCOMMIT", connect_args={}, poolclass=StaticPool)


# Provide a fresh DB session per test
@pytest.fixture()
def db(engine):
    # Set up
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


# ********* TEST ACCOUNT ********************************************************************
@pytest.fixture()
def test_account() -> AccountCreate:
    account_create = AccountCreate(
        uid=TEST_ACCOUNT_UID, email=TEST_ACCOUNT_EMAIL, password=TEST_ACCOUNT_PASSWORD, full_name="Demo User"
    )
    return account_create


@pytest.fixture
def test_account_auth_token(client: TestClient, test_account):
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": test_account.email, "password": test_account.password},
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


@pytest.fixture
def test_account_authorized_headers(test_account_auth_token):
    return {"Authorization": f"Bearer {test_account_auth_token}"}


@pytest.fixture
def test_account_authorized_account_id(test_account_auth_token):
    decoded = jwt.decode(test_account_auth_token, options={"verify_signature": False})
    return decoded["id"]
