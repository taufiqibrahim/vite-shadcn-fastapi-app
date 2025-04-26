import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr, field_validator
from sqlmodel import SQLModel

from src.auth.models import AccountType


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: EmailStr
    id: int
    jti: str
    exp: Optional[int] = None


class TokenRefresh(BaseModel):
    access_token: str
    token_type: str


class AccountBase(BaseModel):
    uid: Optional[uuid.UUID] = None
    email: EmailStr
    disabled: Optional[bool] = False


class AccountCreate(AccountBase):
    password: Optional[SecretStr] = None
    account_type: Optional[AccountType] = AccountType.USER

    @field_validator("password")
    def password_validation(cls, v):
        value = v.get_secret_value()
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one number")

        return value


class AccountCreated(AccountBase):
    id: int
    account_type: Optional[AccountType] = AccountType.USER


class AccountUpdate(SQLModel):
    id: int
    email: Optional[str] = None
    password: Optional[str] = None
