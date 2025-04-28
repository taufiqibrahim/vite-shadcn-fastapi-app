import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.accounts.models import Account


class APIKey(SQLModel, table=True):
    __tablename__ = "api_key"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    key: str = Field(unique=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)
    # account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    # account: Optional["Account"] = Relationship(back_populates="api_keys")
    is_active: bool = True
    level: int = Field(default=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
