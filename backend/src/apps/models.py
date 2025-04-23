import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class App(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)  # Add the uid field
    name: str = Field(unique=True)
    description: Optional[str]
    disabled: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
