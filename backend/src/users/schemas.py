from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
import uuid


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
