import asyncio
import os
import signal
from pydantic_settings import BaseSettings, SettingsConfigDict
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.worker import Worker


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    LOG_LEVEL: str = "warning"


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minio"
    MINIO_SECRET_KEY: str = "changeme123"
    MINIO_BUCKET_NAME: str = "mybucket"
    MINIO_SECURE: bool = False


class PostgisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    POSTGIS_HOST: str = "127.0.0.1"
    POSTGIS_DB: str = "data"
    POSTGIS_USER: str = "app"
    POSTGIS_PASSWORD: str = "changeme123"
    POSTGIS_PORT: str = "5432"


minio_settings = MinioSettings()
postgis_settings = PostgisSettings()


class WorkerApp:
    def __init__(
        self, workflows, activities, task_queue="default-queue", server="localhost:7233"
    ):
        self.workflows = workflows
        self.activities = activities
        self.task_queue = task_queue
        self.server = server
        self.client = None
        self.worker = None

    async def shutdown(self):
        """Gracefully shuts down the worker."""
        print("🚨 Shutdown signal received. Gracefully stopping worker...")
        await self.worker.shutdown()  # Graceful shutdown of worker
        print("✅ Worker stopped gracefully.")

    def handle_shutdown_signal(self):
        """Wrapper function to ensure shutdown is awaited."""
        loop = asyncio.get_event_loop()
        loop.create_task(self.shutdown())

    async def start(self):
        """Start the Temporal worker and handle signals."""
        # Set up the Temporal client
        print("📝 Connecting to Temporal server...")
        self.client = await Client.connect(
            os.getenv("TEMPORAL_SERVER", self.server),
            namespace="default",
            data_converter=pydantic_data_converter,
        )

        # Set up the worker
        self.worker = Worker(
            self.client,
            task_queue=self.task_queue,
            workflows=self.workflows,
            activities=self.activities,
        )
        print(f"🚀 Worker running for task_queue: {self.task_queue}...")

        # Register signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self.handle_shutdown_signal)
        loop.add_signal_handler(signal.SIGTERM, self.handle_shutdown_signal)

        # Start the worker
        await self.worker.run()
