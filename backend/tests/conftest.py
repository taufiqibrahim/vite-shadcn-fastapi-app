from src.auth.models import Account, AccountType
from src.auth.services import get_password_hash
from src.core.logging import setup_logging, get_logger
from src.database.session import get_db
from src.main import app
import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, text, select
from sqlmodel.pool import StaticPool
from src.users.schemas import AccountCreate, UserProfileCreate
from datetime import datetime, timedelta, timezone

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
TEST_SERVICE_ACCOUNT_EMAIL = "service@example.com"
TEST_SERVICE_ACCOUNT_PASSWORD = "service_password"

POSTGRES_SQLALCHEMY_URI = "postgresql://app:changeme123@localhost:5432/postgres"
TESTDB_SQLALCHEMY_URI = "postgresql://app:changeme123@localhost:5432/testdb"


def run_alembic_migration():
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", TESTDB_SQLALCHEMY_URI)
    upgrade(alembic_config, "head")


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


@pytest.fixture(scope="session")
def session_db():
    engine = create_engine(TESTDB_SQLALCHEMY_URI, isolation_level="AUTOCOMMIT", connect_args={}, poolclass=StaticPool)
    with Session(engine) as session:
        yield session


# Provide a fresh DB session per test
@pytest.fixture()
def db():
    # Set up
    engine = create_engine(TESTDB_SQLALCHEMY_URI, isolation_level="AUTOCOMMIT", connect_args={}, poolclass=StaticPool)
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


# ********* TEST ACCOUNT FIXTURES ********************************************************************
@pytest.fixture(scope="session")
def test_account() -> AccountCreate:
    return AccountCreate(
        uid=TEST_ACCOUNT_UID, email=TEST_ACCOUNT_EMAIL, password=TEST_ACCOUNT_PASSWORD, full_name="Test User"
    )


@pytest.fixture(scope="session")
def test_account_db(session_db, test_account) -> Account:
    account = Account(
        email=test_account.email,
        hashed_password=get_password_hash(test_account.password),
        account_type=AccountType.SERVICE_ACCOUNT,
    )
    session_db.add(account)
    session_db.commit()
    session_db.refresh(account)
    return account


# @pytest.fixture
# def test_account_auth_token(test_account_db):
#     data = {
#         "sub": test_account_db.email,
#         "id": test_account_db.id,
#     }

#     # Create token with custom expiration
#     token = create_access_token(data, expires_delta=timedelta(minutes=15))
#     return token

# @pytest.fixture()
# def test_service_account() -> AccountCreate:
#     account_create = AccountCreate(
#         email=TEST_SERVICE_ACCOUNT_EMAIL,
#         password=TEST_SERVICE_ACCOUNT_PASSWORD,
#         account_type=AccountType.SERVICE_ACCOUNT,
#         full_name="Service Account",
#     )
#     return account_create

# @pytest.fixture
# def test_service_account_auth_token(client: TestClient, test_service_account, db):
#     hashed_password = get_password_hash(test_service_account.password)
#     service_account = Account(
#         email=test_service_account.email,
#         hashed_password=hashed_password,
#         account_type=AccountType.SERVICE_ACCOUNT,
#     )
#     db.add(service_account)
#     db.commit()
#     db.refresh(service_account)

#     login_response = client.post(
#         "/api/v1/auth/login",
#         data={"username": test_service_account.email, "password": test_service_account.password},
#     )
#     assert login_response.status_code == 200
#     return login_response.json()["access_token"]


# @pytest.fixture
# def test_account_authorized_headers(test_account_auth_token):
#     return {"Authorization": f"Bearer {test_account_auth_token}"}


# @pytest.fixture
# def test_service_account_authorized_headers(test_service_account_auth_token):
#     return {"Authorization": f"Bearer {test_service_account_auth_token}"}


# @pytest.fixture
# def test_account_authorized_account_id(test_account_auth_token):
#     decoded = jwt.decode(test_account_auth_token, options={"verify_signature": False})
#     return decoded["id"]


# @pytest.fixture
# def test_service_account_authorized_account_id(test_service_account_auth_token):
#     decoded = jwt.decode(test_service_account_auth_token, options={"verify_signature": False})
#     return decoded["id"]


# # ********* API KEY FIXTURES ********************************************************************
# @pytest.fixture
# def test_api_key(db, test_account_authorized_account_id):
#     from src.auth.services import create_api_key

#     return create_api_key(db, test_account_authorized_account_id, level=1)


# @pytest.fixture
# def test_api_key_headers(test_api_key):
#     return {"X-API-Key": test_api_key}


# # ********* USER PROFILE FIXTURES ********************************************************************
# @pytest.fixture
# def test_user_profile() -> UserProfileCreate:
#     return UserProfileCreate(full_name="Test User Profile")


# @pytest.fixture
# def test_user_profile_with_account(db, test_account, test_user_profile):
#     from src.users.services import create_user_profile

#     account = Account(
#         email=test_account.email,
#         hashed_password=get_password_hash(test_account.password),
#         account_type=AccountType.USER,
#     )
#     db.add(account)
#     db.commit()
#     db.refresh(account)

#     profile = create_user_profile(db, account.id, test_user_profile)
#     return profile, account


# @pytest.fixture
# def test_user_profile_headers(test_user_profile_with_account, test_account_auth_token):
#     profile, account = test_user_profile_with_account
#     return {"Authorization": f"Bearer {test_account_auth_token}", "X-Profile-ID": str(profile.id)}
