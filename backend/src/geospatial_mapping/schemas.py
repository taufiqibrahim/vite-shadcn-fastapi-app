from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class DatasetBase(SQLModel):
    account_id: int
    name: str
    description: Optional[str] = None
    file_name: str
    storage_uri: str
    status: str


class DatasetRead(DatasetBase):
    id: int
    uid: uuid.UUID
    created_at: datetime


class DatasetCreate(DatasetBase):
    pass
