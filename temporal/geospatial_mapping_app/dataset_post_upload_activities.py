import logging
from datetime import timedelta
from typing import Any, Dict
from temporalio import activity
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError

from geospatial_mapping_app.models import Dataset, DatasetLoadOgr
from geospatial_mapping_app.functions import (
    fetch_dataset_from_cloud,
    ogr2ogr_to_postgis,
)


@activity.defn
async def validate_input_activity(input_payload: Dict[str, Any]) -> Dataset:
    logging.info("Validating input payload")
    try:
        validated = Dataset(**input_payload)
        return validated
    except Exception as e:
        raise ApplicationError("str(e)", non_retryable=True)


@activity.defn
async def fetch_dataset_from_cloud_activity(dataset: Dataset) -> DatasetLoadOgr:
    logging.info(f"Fetching dataset {dataset.uid} from cloud storage...")
    try:
        fetched = fetch_dataset_from_cloud(dataset)
        return fetched
    except Exception as e:
        raise ApplicationError("str(e)", non_retryable=True)


@activity.defn
async def ogr2ogr_to_postgis_activity(data: DatasetLoadOgr) -> DatasetLoadOgr:
    try:
        ogr2ogr_to_postgis(data=data)
        return data
    except Exception as e:
        raise ApplicationError("str(e)", non_retryable=True)


# @activity.defn
# async def update_metadata_db(dataset_uid: str, status: str) -> str:
#     # Simulate updating dataset metadata status
#     print(f"Updating metadata DB for {dataset_uid} to {status}...")
#     await asyncio.sleep(2)
#     return f"Updated {dataset_uid} to {status} in metadata DB"
