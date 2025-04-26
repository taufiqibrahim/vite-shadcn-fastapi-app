"""Security service for authentication and authorization."""

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/accounts/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
