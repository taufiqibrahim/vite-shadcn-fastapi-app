from fastapi import HTTPException, status


class BaseAPIError(HTTPException):
    """Base class for all API errors."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "GENERIC_ERROR"
    message = "An unexpected error occurred"

    def __init__(self, message: str = None, error_code: str = None):
        self.message = message or self.message
        self.error_code = error_code or self.error_code

        super().__init__(
            status_code=self.status_code,
            detail={"error_code": self.error_code, "message": self.message},
        )


class APINotImplementedError(BaseAPIError):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    error_code = "API_NOT_IMPLEMENTED_ERROR"
    message = "API not implemented"


class ServiceNotImplementedError(BaseAPIError):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    error_code = "SERVICE_NOT_IMPLEMENTED_ERROR"
    message = "Service not implemented"


class CredentialsValidationFailureException(BaseAPIError):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "CREDENTIALS_VALIDATION_FAILURE_EXCEPTION"
    message = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


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
