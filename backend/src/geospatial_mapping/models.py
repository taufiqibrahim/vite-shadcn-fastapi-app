from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlmodel import TIMESTAMP, Column, SQLModel, Field
from enum import Enum


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

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP, onupdate=datetime.now(timezone.utc)),
    )
