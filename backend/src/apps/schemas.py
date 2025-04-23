import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel


class AppRead(SQLModel):
    id: int
    uid: uuid.UUID
    name: str
    description: Optional[str]
    disabled: bool
    created_at: datetime


class AppCreate(BaseModel):
    name: str
    description: Optional[str] = ""
