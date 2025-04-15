# import uuid
from sqlmodel import Session, select
from src.geospatial_mapping.models import Dataset
from src.geospatial_mapping.schemas import DatasetCreate
from src.core.logging import get_logger

logger = get_logger(__name__)


def create_dataset(db: Session, dataset: DatasetCreate):
    logger.debug(f"create_dataset {dataset}")
    db_dataset = Dataset(**dataset.model_dump())
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


def list_datasets(db: Session, account_id: int, skip: int = 0, limit: int = 100):
    return db.exec(select(Dataset).where(Dataset.account_id == account_id).offset(skip).limit(limit)).all()
