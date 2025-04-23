from fastapi import status
from src.core.exceptions import BaseAPIError


class AccountDisabledException(BaseAPIError):
    """Raised when authenticates with disabled account."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "ACCOUNT_DISABLED"
    message = "Account disabled"


class EmailAlreadyExistsException(BaseAPIError):
    """Raised when trying to register with an email that already exists."""

    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "EMAIL_ALREADY_EXISTS"
    message = "Account with this email already exists"


class InvalidLoginCredentialsException(BaseAPIError):
    """Raised when login with invalid credentials."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "INVALID_LOGIN_CREDENTIALS"
    message = "Invalid login credentials"


class InvalidAccessTokenException(BaseAPIError):
    """Raised when authenticates with invalid access token."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "INVALID_ACCESS_TOKEN"
    message = "Invalid access token"
