from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlmodel import SQLModel, Field


class AppBase(SQLModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class App(AppBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AppCreate(AppBase):
    pass

class AppsPublic(SQLModel):
    data: list[App]
    count: int
