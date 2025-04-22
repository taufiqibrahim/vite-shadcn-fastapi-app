from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, Column
import uuid


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profile"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)
    full_name: str
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    account: Optional["Account"] = Relationship(back_populates="profile")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
