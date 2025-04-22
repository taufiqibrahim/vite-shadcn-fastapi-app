from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
import uuid

from src.auth.models import AccountType


class AccountBase(SQLModel):
    uid: Optional[uuid.UUID] = None
    email: EmailStr
    disabled: Optional[bool] = False


class AccountCreate(AccountBase):
    password: Optional[str] = None
    full_name: Optional[str] = None
    account_type: Optional[AccountType] = AccountType.USER


class UserProfileBase(SQLModel):
    account_id: int
    full_name: str


class UserProfileCreate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: uuid.UUID


class UserAccount(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: uuid.UUID
    account_type: str
