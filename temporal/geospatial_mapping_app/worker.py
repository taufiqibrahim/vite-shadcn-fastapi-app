import asyncio
import os
from base import WorkerApp, settings
from geospatial_mapping_app.dataset_post_upload_workflows import (
    DatasetPostUploadWorkflow,
)
from geospatial_mapping_app.dataset_post_upload_activities import (
    fetch_dataset_from_cloud_activity,
    ogr2ogr_to_postgis_activity,
    validate_input_activity,
    update_dataset_metadata_activity,
)

TASK_QUEUE = "default-queue"


if __name__ == "__main__":
    worker_app = WorkerApp(
        workflows=[DatasetPostUploadWorkflow],
        activities=[
            validate_input_activity,
            fetch_dataset_from_cloud_activity,
            ogr2ogr_to_postgis_activity,
            update_dataset_metadata_activity,
        ],
        task_queue="default-queue",
        server=settings.TEMPORAL_ADDRESS
    )
    asyncio.run(worker_app.start())
