import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
import os

from workflows import DatasetPostUploadWF, x_sleep

TASK_QUEUE = "geospatial-mapping-app-queue"


async def main():
    client = await Client.connect(
        os.getenv("TEMPORAL_SERVER", "localhost:7233"), namespace="default"
    )
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[DatasetPostUploadWF],
        activities=[x_sleep],
    )
    print(f"🚀 Worker started, listening to task_queue: {TASK_QUEUE}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
