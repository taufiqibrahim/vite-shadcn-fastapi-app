import asyncio
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select
from temporalio.client import Client as TemporalClient
from src.auth.models import Account
from src.auth.services import get_current_active_account, get_current_active_account_or_400
from src.database.session import get_db
from src.dependencies import get_temporal_client
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
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account_or_400),
    temporal_client: TemporalClient = Depends(get_temporal_client),
):
    # check if record exists by file_name
    db_dataset_count = db.exec(select(func.count(Dataset.id)).where(Dataset.file_name == dataset.file_name)).one()
    dataset.account_id = account.id

    # increment default name + 1 if same filename uploaded more than once
    if db_dataset_count == 1:
        dataset.name = f"{dataset.name} (1)"
    elif db_dataset_count > 1:
        dataset.name = f"{dataset.name} ({db_dataset_count})"

    db_dataset = services.create_dataset(db=db, dataset=dataset)

    # trigger temporal job async
    await temporal_client.start_workflow(
        "DatasetPostUploadWorkflow",
        db_dataset.model_dump(mode="json"),
        id=f"post-create-dataset-{uuid.uuid4()}",
        task_queue="default-queue",
    )

    return db_dataset


@router.get("/datasets", response_model=List[DatasetRead])
async def list_datasets(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
):
    datasets = services.list_datasets(db, account_id=account.id, skip=skip, limit=limit)
    return datasets


@router.get("/datasets/{account_id}", response_model=DatasetRead)
async def read_user(
    account_id: int,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
):
    db_account = services.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account
