from typing import Optional
from pydantic import BaseModel


class Dataset(BaseModel):
    id: int
    uid: str
    account_id: int
    name: str
    description: Optional[str] = None
    file_name: str
    storage_backend: str
    storage_uri: str
    status: str
    created_at: str


class DatasetLoadOgr(BaseModel):
    uid: str
    tmp_dir: str
    tmp_file_path: str
