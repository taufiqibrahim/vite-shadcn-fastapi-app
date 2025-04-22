"""JWT service for token handling."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import ExpiredSignatureError, JWTError, jwt
from jwt import InvalidSignatureError
from src.core.config import settings, secret_settings
from src.auth import schemas
from src.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": data["sub"]})
    encoded_jwt = jwt.encode(to_encode, secret_settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_and_validate_token(token: str) -> Optional[schemas.TokenPayload]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token to decode and validate

    Returns:
        Optional[TokenPayload]: Token payload if valid, None otherwise
    """
    try:
        # Decode and verify signature
        payload = jwt.decode(token, secret_settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Parse payload into schema
        token_data = schemas.TokenPayload(**payload)

        # Validate expiration manually (if your schema doesn't use auto-validation)
        if token_data.exp and datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(timezone.utc):
            return None

        # Add more claim checks here if needed (e.g. aud, iss)

        return token_data

    except (JWTError, InvalidSignatureError, ExpiredSignatureError, ValueError) as e:
        print(str(e))
        raise e
