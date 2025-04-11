from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
import uuid

class AccountBase(SQLModel):
    email: EmailStr
    disabled: Optional[bool] = False


class AccountCreate(AccountBase):
    password: str
    account_type: str

class UserProfileBase(SQLModel):
    email: EmailStr
    full_name: str

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: uuid.UUID  # Add uid

class Account(AccountBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: uuid.UUID # Add uid
    account_type: str
