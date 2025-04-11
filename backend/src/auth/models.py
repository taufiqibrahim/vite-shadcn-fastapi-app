from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Enum, Column
import enum
import uuid


class AccountType(enum.Enum):
    USER = "user"
    SERVICE_ACCOUNT = "service-account"


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)  # Add the uid field
    email: str = Field(unique=True, index=True)
    hashed_password: Optional[str]
    disabled: bool = False
    account_type: AccountType = Field(sa_column=Column(Enum(AccountType)), default=AccountType.USER) # Add the account type
    api_keys: List["APIKey"] = Relationship(back_populates="account")
    profile: Optional["UserProfile"] = Relationship(back_populates="account") # Add profile relationship


class APIKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    key: str = Field(unique=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)  # Add the uid field
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    account: Optional[Account] = Relationship(back_populates="api_keys")
    is_active: bool = True
    level: int = Field(default=1) # Add a level for the API key


class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)  # Add the uid field
    full_name: str
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    account: Optional[Account] = Relationship(back_populates="profile")
