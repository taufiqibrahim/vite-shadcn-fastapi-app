from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: str
    full_name: Optional[str] = None
    is_active: bool = True


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # TODO: store provider (google, github, etc)
    auth_provider: str = "local"


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
