from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from geospatial_mapping_app.dataset_post_upload_activities import (
        fetch_dataset_from_cloud_activity,
        ogr2ogr_to_postgis_activity,
        update_dataset_metadata_activity,
        validate_input_activity,
    )


@workflow.defn(name="DatasetPostUploadWorkflow")
class DatasetPostUploadWorkflow:
    @workflow.run
    async def run(self, dataset: dict) -> str:

        # Validate input payload
        validated = await workflow.execute_activity(
            validate_input_activity,
            dataset,
            schedule_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(maximum_attempts=1),
        )

        # Fetch dataset from cloud
        fetched = await workflow.execute_activity(
            fetch_dataset_from_cloud_activity,
            validated,
            schedule_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        # Load dataset to PostGIS
        loaded = await workflow.execute_activity(
            ogr2ogr_to_postgis_activity,
            fetched,
            schedule_to_close_timeout=timedelta(minutes=30),
            retry_policy=RetryPolicy(maximum_attempts=3)
        )

        # Update Dataset metadata
        data = await workflow.execute_activity(
            update_dataset_metadata_activity,
            loaded,
            schedule_to_close_timeout=timedelta(minutes=30),
            retry_policy=RetryPolicy(maximum_attempts=3)
        )

