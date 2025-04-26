from unittest.mock import patch

import pytest
from fastapi import status
from pydantic import SecretStr

from src.auth.exceptions import AccountDisabledException, EmailAlreadyExistsException, InvalidLoginCredentialsException
from src.auth.services.security import get_password_hash
from src.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

from src.auth.models import Account, AccountType
from src.auth.schemas import AccountCreate


# ********* AUTH TESTS *********
@pytest.mark.asyncio
async def test_login_success(client, test_account):
    """Test successful login with correct credentials"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_account.email, "password": test_account.password},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_email_case_insensitive(client, test_account):
    """Test login is case-insensitive on email field"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_account.email.upper(), "password": test_account.password},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    error = response.json()
    assert error["detail"]["error_code"] == InvalidLoginCredentialsException.error_code
    assert error["detail"]["message"] == InvalidLoginCredentialsException.message


@pytest.mark.asyncio
async def test_login_disabled_account(client, db):
    """Test login attempt with disabled account"""
    disabled_account = AccountCreate(
        email="disabled@example.com",
        password=SecretStr("Password123"),
        disabled=True,
        account_type=AccountType.USER,
    )
    db_account = Account(
        email=disabled_account.email,
        hashed_password=get_password_hash(disabled_account.password),
        disabled=True,
        account_type=AccountType.USER,
    )
    db.add(db_account)
    db.commit()

    response = client.post(
        "/api/v1/auth/login",
        data={"username": disabled_account.email, "password": disabled_account.password},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    error = response.json()
    assert error["detail"]["error_code"] == AccountDisabledException.error_code
    assert error["detail"]["message"] == AccountDisabledException.message


@pytest.mark.asyncio
async def test_login_missing_credentials(client):
    """Test login fails with missing username or password"""
    response = client.post(
        "/api/v1/auth/login",
        data={"password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ********* JWT ACCESS TOKEN TESTS *********
@pytest.mark.asyncio
async def test_refresh_token_succesful(client, test_random_account_refresh_token):
    response = client.post(
        "/api/v1/auth/refresh_token", headers={"authorization": "Bearer " + test_random_account_refresh_token}
    )
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"


# ********* TODO: OAUTH TESTS *********
# @pytest.mark.asyncio
# async def test_oauth_login_success(client):
#     """Test successful OAuth login"""
#     # Simulate OAuth login with a third-party provider
#     assert False


# @pytest.mark.asyncio
# async def test_oauth_login_failure(client):
#     """Test failed OAuth login due to invalid token or user denial"""
#     # Simulate failure of OAuth login
#     assert False


# @pytest.mark.asyncio
# async def test_oauth_account_linking(client, test_account):
#     """Test linking OAuth account to an existing user"""
#     # Simulate OAuth account linking for an existing user
#     assert False


# ********* TODO: OTP TESTS *********
# @pytest.mark.asyncio
# async def test_otp_request(client):
#     """Test sending OTP to the user's email or phone"""
#     # Simulate OTP request
#     assert False


# @pytest.mark.asyncio
# async def test_otp_validation_success(client):
#     """Test validating OTP successfully"""
#     # Simulate OTP validation success
#     assert False


# @pytest.mark.asyncio
# async def test_otp_validation_failure(client):
#     """Test failed OTP validation due to incorrect OTP"""
#     # Simulate OTP validation failure
#     assert False


# @pytest.mark.asyncio
# async def test_otp_expiry(client):
#     """Test OTP expiry after a certain period"""
#     # Simulate OTP expiry
#     assert False


# ********* TODO: MAGIC LINK TESTS *********
# @pytest.mark.asyncio
# async def test_magic_link_request(client):
#     """Test sending magic link to the user's email"""
#     # Simulate magic link request
#     assert False


# @pytest.mark.asyncio
# async def test_magic_link_validation_success(client):
#     """Test successful login using the magic link"""
#     # Simulate magic link validation success
#     assert False


# @pytest.mark.asyncio
# async def test_magic_link_expiry(client):
#     """Test magic link expiry after a certain period"""
#     # Simulate magic link expiry
#     assert False


# ********* SIGNUP TESTS *********
@patch("src.auth.api.v1.auth.send_welcome_email")
@pytest.mark.asyncio
async def test_signup_user(mock_send_email, client, test_random_account):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/signup",
        data={
            "email": test_random_account.email,
            "password": test_random_account.password,
        },
    )
    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in data
    assert "refresh_token" in data
    mock_send_email.assert_awaited_once()


@pytest.mark.asyncio
async def test_signup_user_existing_email(client, test_account):
    """Test registration with existing email"""
    response = client.post(
        "/api/v1/auth/signup",
        data={
            "email": test_account.email,
            "password": test_account.password,
        },
    )
    error = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error["detail"]["error_code"] == EmailAlreadyExistsException.error_code
    assert error["detail"]["message"] == EmailAlreadyExistsException.message


@pytest.mark.asyncio
async def test_signup_weak_password(client, test_random_account):
    """Test signup fails if password does not meet strength requirements"""
    response = client.post(
        "/api/v1/auth/signup",
        data={
            "email": test_random_account.email,
            "password": "weakpass",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_signup_invalid_email_format(client, test_random_account):
    """Test signup fails with invalid email format"""
    account = {"email": test_random_account.email.replace("@", "2"), "password": test_random_account.password}
    response = client.post("/api/v1/auth/signup", json=account)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_signup_missing_required_fields(client, test_random_account):
    """Test signup fails when required fields are missing"""
    account = {"email": "missing_password@example.com"}
    response = client.post("/api/v1/auth/signup", json=account)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    account = {"password": test_random_account.password}
    response = client.post("/api/v1/auth/signup", json=account)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# @pytest.mark.asyncio
# async def test_logout_user(client):
#     """Test user logout and token invalidation (if implemented)"""
#     assert False


# ********* TODO: OTHER RECOMMENDED TESTS *********
# @pytest.mark.asyncio
# async def test_refresh_token_invalid(client):
#     """Test refresh token endpoint fails with invalid or malformed token"""
#     pass

# @pytest.mark.asyncio
# async def test_refresh_token_missing(client):
#     """Test refresh token endpoint fails when token is missing"""
#     pass

# @pytest.mark.asyncio
# async def test_logout_token_reuse(client):
#     """Test that token cannot be reused after logout (if supported)"""
#     pass

# @pytest.mark.asyncio
# async def test_logout_twice(client):
#     """Test logging out twice with the same token (idempotent behavior or 401)"""
#     pass

# @pytest.mark.asyncio
# async def test_password_reset_request_valid(client):
#     """Test sending password reset request for valid registered email"""
#     pass

# @pytest.mark.asyncio
# async def test_password_reset_request_invalid(client):
#     """Test sending password reset request for unregistered email"""
#     pass

# @pytest.mark.asyncio
# async def test_password_reset_confirm_valid(client):
#     """Test confirming new password with valid reset token"""
#     pass

# @pytest.mark.asyncio
# async def test_password_reset_confirm_invalid(client):
#     """Test password reset confirmation with invalid/expired token"""
#     pass

# @pytest.mark.asyncio
# async def test_login_rate_limit(client):
#     """Test repeated failed logins trigger rate limit (if implemented)"""
#     pass
