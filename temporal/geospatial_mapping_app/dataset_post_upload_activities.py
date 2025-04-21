import logging
from datetime import timedelta
from typing import Any, Dict
from temporalio import activity
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError

from geospatial_mapping_app.models import Dataset, DatasetLoadOgr
from geospatial_mapping_app.functions import (
    fetch_dataset_from_cloud,
    notify_backend,
    ogr2ogr_to_postgis,
    update_dataset_metadata,
)


@activity.defn
async def validate_input_activity(input_payload: Dict[str, Any]) -> Dataset:
    logging.info("Validating input payload")
    try:
        validated = Dataset(**input_payload)
        notify_backend(dataset_uid=validated.uid, dataset_update={"status": "processing"})
        return validated
    except Exception as e:
        notify_backend(dataset_uid=validated.uid, dataset_update={"status": "failed"})
        raise ApplicationError(str(e), non_retryable=True)


@activity.defn
async def fetch_dataset_from_cloud_activity(dataset: Dataset) -> DatasetLoadOgr:
    logging.info(f"Fetching dataset {dataset.uid} from cloud storage...")
    try:
        fetched = fetch_dataset_from_cloud(dataset)
        return fetched
    except Exception as e:
        notify_backend(dataset_uid=dataset.uid, dataset_update={"status": "failed"})
        raise ApplicationError(str(e), non_retryable=True)


@activity.defn
async def ogr2ogr_to_postgis_activity(data: DatasetLoadOgr) -> DatasetLoadOgr:
    try:
        ogr2ogr_to_postgis(data=data)
        return data
    except Exception as e:
        notify_backend(dataset_uid=data.uid, dataset_update={"status": "failed"})
        raise ApplicationError(str(e), non_retryable=True)

@activity.defn
async def update_dataset_metadata_activity(data: DatasetLoadOgr) -> DatasetLoadOgr:
    try:
        dataset_update = update_dataset_metadata(data=data)
        notify_backend(dataset_uid=data.uid, dataset_update=dataset_update)
    except Exception as e:
        notify_backend(dataset_uid=data.uid, dataset_update={"status": "failed"})
        raise ApplicationError(str(e), non_retryable=True)
