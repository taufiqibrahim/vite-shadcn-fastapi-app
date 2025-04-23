import enum
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from src.users.models import UserProfile


class AccountType(enum.Enum):
    USER = "user"
    SERVICE_ACCOUNT = "service-account"


class Account(SQLModel, table=True):
    __tablename__ = "account"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: Optional[str]
    disabled: bool = False
    account_type: AccountType = Field(sa_column=Column(Enum(AccountType)), default=AccountType.USER)
    api_keys: List["APIKey"] = Relationship(back_populates="account")
    profile: Optional[UserProfile] = Relationship(back_populates="account")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class APIKey(SQLModel, table=True):
    __tablename__ = "api_key"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    key: str = Field(unique=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    account: Optional[Account] = Relationship(back_populates="api_keys")
    is_active: bool = True
    level: int = Field(default=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
