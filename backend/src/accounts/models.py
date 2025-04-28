import enum
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Enum, Field, Relationship, SQLModel

from src.organizations.models import Organization


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
    account_type: AccountType = Field(
        sa_column=Column(Enum(AccountType)), default=AccountType.USER
    )

    # List of organizations owned by this account
    organizations: list["Organization"] = Relationship(back_populates="account")

    # The profile record of this account
    profile: Optional["AccountProfile"] = Relationship(back_populates="account")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP, onupdate=datetime.now(timezone.utc)),
    )


class AccountProfile(SQLModel, table=True):
    __tablename__ = "account_profile"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)
    full_name: str
    account_id: Optional[int] = Field(
        default=None, foreign_key="account.id", unique=True
    )
    account: Optional["Account"] = Relationship(back_populates="profile")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP, onupdate=datetime.now(timezone.utc)),
    )
