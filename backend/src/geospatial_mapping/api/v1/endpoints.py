from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select
from src.auth.models import Account
from src.auth.services import get_current_active_account_or_400
from src.database.session import get_db
from src.geospatial_mapping.models import Dataset
from src.geospatial_mapping.schemas import DatasetCreate, DatasetRead
from src.geospatial_mapping import services

router = APIRouter(
    prefix="/api/v1/geospatial-mapping",
    tags=["Geospatial Mapping"],
    dependencies=[Depends(get_current_active_account_or_400)],
)


@router.post("/datasets", status_code=status.HTTP_201_CREATED)
async def create_dataset(
    dataset: DatasetCreate, db: Session = Depends(get_db), account: Account = Depends(get_current_active_account_or_400)
):
    db_dataset_count = db.exec(select(func.count(Dataset.id)).where(Dataset.name == dataset.name)).one()
    dataset.account_id = account.id

    if db_dataset_count > 0:
        dataset.name = f"{dataset.name} ({db_dataset_count + 1})"

    db_dataset = services.create_dataset(db=db, dataset=dataset)

    return db_dataset


@router.get("/datasets", response_model=List[DatasetRead])
async def list_datasets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account_or_400),
):
    apps = services.list_datasets(db, account_id=account.id, skip=skip, limit=limit)
    return apps
