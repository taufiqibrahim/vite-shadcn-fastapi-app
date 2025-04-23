from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr
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
    disabled: Optional[bool] = True


class AccountCreate(AccountBase):
    password: Optional[str] = None
    account_type: Optional[AccountType] = AccountType.USER


class AccountCreated(AccountBase):
    id: int
    account_type: Optional[AccountType] = AccountType.USER
