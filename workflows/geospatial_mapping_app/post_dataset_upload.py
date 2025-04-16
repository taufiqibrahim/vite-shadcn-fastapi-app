from datetime import timedelta
from temporalio import workflow, activity
import asyncio
import os


@activity.defn
async def get_dataset_from_cloud(dataset_id: str) -> str:
    # Simulate fetching from cloud storage
    print(f"Fetching dataset {dataset_id} from cloud storage...")
    await asyncio.sleep(2)  # Simulate cloud fetch delay
    return f"Dataset {dataset_id} fetched"


@activity.defn
async def convert_to_postgis_format(dataset_path: str) -> str:
    # Simulate dataset conversion
    print(f"Converting dataset {dataset_path} to PostGIS format...")
    await asyncio.sleep(3)
    return f"Converted {dataset_path} to PostGIS format"


@activity.defn
async def load_to_postgis(dataset_path: str) -> str:
    # Simulate loading data to PostGIS
    print(f"Loading {dataset_path} to PostGIS...")
    await asyncio.sleep(5)
    return f"Loaded {dataset_path} to PostGIS"


@activity.defn
async def create_pmtile_if_needed(dataset_size: float, dataset_path: str) -> str:
    # Only create PMTile if dataset is > 10MB
    if dataset_size > 10:
        print(f"Creating PMTile for dataset {dataset_path} (size: {dataset_size}MB)...")
        await asyncio.sleep(4)
        return f"PMTile created for {dataset_path}"
    return f"No PMTile needed for {dataset_path}"


@activity.defn
async def update_metadata_db(dataset_id: str, status: str) -> str:
    # Simulate updating dataset metadata status
    print(f"Updating metadata DB for {dataset_id} to {status}...")
    await asyncio.sleep(2)
    return f"Updated {dataset_id} to {status} in metadata DB"


@workflow.defn(name="DatasetPostUploadWorkflow")
class DatasetPostUploadWorkflow:
    @workflow.run
    async def run(self, dataset_id: str, dataset_size: float) -> str:
        # Fetch dataset from cloud
        print(f"[Workflow] Starting workflow for dataset {dataset_id}")
        dataset_path = await workflow.execute_activity(
            get_dataset_from_cloud,
            dataset_id,
            schedule_to_close_timeout=timedelta(minutes=10),
        )

        # Convert dataset to PostGIS format
        converted_path = await workflow.execute_activity(
            convert_to_postgis_format,
            dataset_path,
            schedule_to_close_timeout=timedelta(minutes=15),
        )

        # Load dataset to PostGIS
        await workflow.execute_activity(
            load_to_postgis,
            converted_path,
            schedule_to_close_timeout=timedelta(minutes=30),
        )

        # Create PMTile if dataset size > 10MB
        pmtile_status = await workflow.execute_activity(
            create_pmtile_if_needed,
            dataset_size,
            dataset_path,
            schedule_to_close_timeout=timedelta(minutes=20),
        )

        # Update metadata DB status to "ready"
        await workflow.execute_activity(
            update_metadata_db,
            dataset_id,
            "ready",
            schedule_to_close_timeout=timedelta(minutes=5),
        )

        return f"Workflow completed for {dataset_id} with status: {pmtile_status}"
