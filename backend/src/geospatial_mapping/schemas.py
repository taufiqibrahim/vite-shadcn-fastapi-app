from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class DatasetBase(SQLModel):
    name: str
    description: Optional[str]
    status: str


class DatasetRead(DatasetBase):
    id: int
    uid: uuid.UUID
    account_id: int
    name: str
    description: Optional[str]
    file_name: str
    storage_uri: str
    status: str
    created_at: datetime


class DatasetCreate(DatasetBase):
    account_id: Optional[int] = None
    file_name: str
    storage_uri: str
