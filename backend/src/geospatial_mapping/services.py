# import uuid
import asyncio
import uuid
from fastapi import HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select, text
from src.geospatial_mapping.models import Dataset, DatasetCreate, DatasetUpdate
from src.core.logging import get_logger
from src.utils import stream_json

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


def update_dataset(db: Session, dataset_uid: str, account_id: int, dataset: DatasetUpdate):
    logger.debug(f"update_dataset {dataset}")

    db_dataset = db.exec(select(Dataset).where(Dataset.uid == dataset_uid)).first()
    if not db_dataset:
        raise HTTPException(status_code=404, detail="Not found")

    # Apply updates from the request payload
    update_data = dataset.model_dump(exclude_unset=True)
    print(update_data)
    for key, value in update_data.items():
        setattr(db_dataset, key, value)

    # Commit the changes and refresh the instance
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)

    return db_dataset


def get_dataset_bbox(db: Session, dataset_uid: str) -> dict:
    dataset = db.exec(select(Dataset).where(Dataset.uid == dataset_uid)).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Not found")
    table_name = f"u_{str(dataset_uid).replace('-', '_')}"
    query = text(
        f"""SELECT
        JSON_BUILD_OBJECT(
            'xmin', ST_XMin(extent),
            'ymin', ST_YMin(extent),
            'xmax', ST_XMax(extent),
            'ymax', ST_YMax(extent)
        ) AS bbox
        FROM (
        SELECT ST_Extent(geom) AS extent
        FROM {table_name}
        ) AS sub"""
    )
    result = db.exec(query).mappings().first()
    return result.bbox


def get_dataset_by_uid(db: Session, dataset_uid: str, account_id: int):
    db_dataset = db.exec(select(Dataset).where(Dataset.account_id == account_id, Dataset.uid == dataset_uid)).first()
    if not db_dataset:
        raise HTTPException(status_code=404, detail="Not found")
    return db_dataset


def get_dataset_as_table_by_uid(db: Session, dataset_uid: str, account_id: int, limit: int, offset: int):
    dataset = db.exec(select(Dataset).where(Dataset.account_id == account_id, Dataset.uid == dataset_uid)).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Not found")

    table_name = f"u_{dataset_uid.replace('-', '_')}"
    query = text(f"SELECT * FROM {table_name} LIMIT :limit OFFSET :offset")
    records = db.exec(query.params(limit=limit, offset=offset)).mappings().all()

    return StreamingResponse(stream_json(records), media_type="application/json")


EMPTY_TILE = b"\x1a\x00"


def get_dataset_as_mvt_by_uid(db: Session, dataset_uid: str, primary_key_column: str, z: int, x: int, y: int):
    relation_name = "u_" + dataset_uid.replace("-", "_")
    stmt = text("SELECT public.get_dataset_tile(:relation, :primary_key_column, :z, :x, :y)")
    result = db.exec(stmt.params(relation=relation_name, primary_key_column=primary_key_column, z=z, x=x, y=y)).scalar()

    if not result or result is None:
        return Response(content=EMPTY_TILE, media_type="application/x-protobuf")

    return Response(content=bytes(result), media_type="application/x-protobuf")
