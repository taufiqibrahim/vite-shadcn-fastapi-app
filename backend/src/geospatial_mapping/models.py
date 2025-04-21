from datetime import datetime, timezone
from typing import Optional
import uuid
from pydantic import BaseModel
from sqlalchemy import JSON
from sqlmodel import TIMESTAMP, Column, Relationship, SQLModel, Field
from enum import Enum

from src.auth.models import Account


class DatasetStatus(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    failed = "failed"


class StorageBackend(str, Enum):
    minio = "minio"
    s3 = "s3"
    https = "https"
    sql = "sql"
    bigquery = "bigquery"


class BoundingBox(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float


class DatasetBase(SQLModel):
    name: str
    description: Optional[str] = None
    file_name: str
    storage_backend: StorageBackend
    storage_uri: str
    status: DatasetStatus = Field(default=DatasetStatus.uploaded)
    bbox: Optional[BoundingBox] = None
    primary_key_column: Optional[str] = None


class DatasetCreate(DatasetBase):
    account_id: int
    uid: Optional[uuid.UUID] = None


class DatasetRead(DatasetBase):
    uid: uuid.UUID
    account_id: int
    created_at: datetime
    updated_at: datetime


class DatasetUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    file_name: Optional[str] = None
    storage_backend: Optional[StorageBackend] = None
    storage_uri: Optional[str] = None
    status: Optional[DatasetStatus] = None
    bbox: Optional[BoundingBox] = None
    primary_key_column: Optional[str] = None


class Dataset(SQLModel, table=True):
    __tablename__ = "dataset"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)
    account_id: int = Field(foreign_key="account.id")
    name: str = Field(unique=True)
    description: Optional[str]
    file_name: str
    storage_backend: StorageBackend
    storage_uri: str
    status: DatasetStatus = Field(default=DatasetStatus.uploaded)
    bbox: Optional[BoundingBox] = Field(default=None, sa_column=Column(JSON))
    primary_key_column: Optional[str]

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP, onupdate=datetime.now(timezone.utc)),
    )
