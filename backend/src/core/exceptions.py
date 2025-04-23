from fastapi import HTTPException, status


class BaseAPIError(HTTPException):
    """Base class for all API errors."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "GENERIC_ERROR"
    message = "An unexpected error occurred"

    def __init__(self, message: str = None, error_code: str = None):
        self.message = message or self.message
        self.error_code = error_code or self.error_code

        super().__init__(status_code=self.status_code, detail={"error_code": self.error_code, "message": self.message})
