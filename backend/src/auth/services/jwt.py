"""JWT service for token handling."""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Header
from jose import ExpiredSignatureError, JWTError, jwt
from jwt import InvalidSignatureError

from src.auth import schemas
from src.auth.exceptions import InvalidAccessTokenException
from src.core.config import secret_settings, settings
from src.core.logging import get_logger, setup_logging

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
    to_encode.update(
        {
            "exp": expire,
            "sub": data["sub"],
            "jti": str(uuid.uuid4()),
        }
    )
    encoded_jwt = jwt.encode(to_encode, secret_settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a new refresh token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update(
        {
            "exp": expire,
            "sub": data["sub"],
            "jti": str(uuid.uuid4()),
        }
    )
    encoded_jwt = jwt.encode(to_encode, secret_settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> Optional[schemas.TokenPayload]:
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
            raise InvalidAccessTokenException

        # Add more claim checks here if needed (e.g. aud, iss)

        return token_data

    except (JWTError, InvalidSignatureError, ExpiredSignatureError, ValueError) as e:
        logger.debug(f"verify_access_token: token={token}")
        logger.debug(f"verify_access_token: {e}")
        raise e


def get_refresh_token(authorization: str = Header(...)) -> str:
    """Extract the refresh token from the Authorization header"""
    if not authorization.startswith("Bearer "):
        raise InvalidAccessTokenException
    return authorization[7:]


def refresh_access_token(refresh_token: str) -> str:
    """Refresh access token using the refresh token"""
    payload = verify_access_token(refresh_token)
    email = payload.sub
    if not email:
        raise Exception("Invalid refresh token")

    access_token = create_access_token(data={"sub": email})
    return access_token
