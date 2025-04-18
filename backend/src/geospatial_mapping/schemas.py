from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import SQLModel


class DatasetBase(SQLModel):
    account_id: int
    uid: uuid.UUID
    name: str
    description: Optional[str] = None
    file_name: str
    storage_backend: str
    storage_uri: str
    status: str


class DatasetRead(DatasetBase):
    id: int
    created_at: datetime


class DatasetCreate(DatasetBase):
    pass
