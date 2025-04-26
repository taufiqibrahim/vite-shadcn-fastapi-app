import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, func, select
from temporalio.client import Client as TemporalClient

from src.auth.models import Account
from src.auth.services import get_current_active_account
from src.core.database import get_db
from src.core.logging import get_logger, setup_logging
from src.dependencies import get_temporal_client
from src.geospatial_mapping import services
from src.geospatial_mapping.models import (
    Dataset,
    DatasetCreate,
    DatasetRead,
    DatasetUpdate,
)

setup_logging()
logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/geospatial-mapping",
    tags=["Geospatial Mapping"],
    dependencies=[Depends(get_current_active_account)],
)


@router.post("/datasets", status_code=status.HTTP_201_CREATED)
async def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
    temporal_client: TemporalClient = Depends(get_temporal_client),
):
    # check if record exists by file_name
    db_dataset_count = db.exec(
        select(func.count(Dataset.id)).where(Dataset.file_name == dataset.file_name)
    ).one()
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
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
):
    datasets = services.list_datasets(db, account_id=account.id, skip=skip, limit=limit)
    return datasets


@router.put("/datasets/{dataset_uid}")
async def update_dataset(
    dataset_uid: str,
    dataset: DatasetUpdate,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
):
    dataset = services.update_dataset(
        db, dataset_uid=dataset_uid, account_id=account.id, dataset=dataset
    )
    return dataset


@router.get("/datasets/{dataset_uid}", response_model=DatasetRead)
async def get_dataset_by_uid(
    dataset_uid: str,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
):
    dataset = services.get_dataset_by_uid(
        db, dataset_uid=dataset_uid, account_id=account.id
    )
    return dataset


@router.get("/datasets/{dataset_uid}/table")
async def get_dataset_as_table_by_uid(
    dataset_uid: str,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
    limit: int = Query(10, gt=0, le=10000),
    offset: int = Query(0, ge=0),
):
    res = services.get_dataset_as_table_by_uid(
        db=db,
        dataset_uid=dataset_uid,
        account_id=account.id,
        limit=limit,
        offset=offset,
    )
    return res


@router.get("/datasets/{dataset_uid}/features")
async def get_dataset_as_geojson_by_uid(
    dataset_uid: str,
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
    bbox: Optional[str] = Query(None, description="Bounding box: xmin,ymin,xmax,ymax"),
):
    res = services.get_dataset_as_geojson_by_uid(
        db=db, dataset_uid=dataset_uid, account_id=account.id, bbox=bbox
    )
    return res


@router.get("/datasets/{dataset_uid}/tiles/{z}/{x}/{y}.pbf")
async def get_dataset_as_mvt_by_uid(
    z: int,
    x: int,
    y: int,
    dataset_uid: uuid.UUID,
    primary_key_column: str = Query("ogc_fid"),
    db: Session = Depends(get_db),
    account: Account = Depends(get_current_active_account),
):
    try:
        return services.get_dataset_as_mvt_by_uid(
            db=db,
            dataset_uid=str(dataset_uid),
            primary_key_column=primary_key_column,
            z=z,
            x=x,
            y=y,
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=f"Tile generation failed: {str(e)}")
