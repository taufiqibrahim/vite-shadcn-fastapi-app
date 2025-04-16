from datetime import timedelta
from temporalio import workflow, activity
import asyncio


@activity.defn
async def x_sleep(seconds: int):
    print(f"[Activity] Sleeping for {seconds} seconds...")
    await asyncio.sleep(seconds)
    return f"Slept for {seconds} seconds"


@workflow.defn(name="DatasetPostUploadWF")  # 👈 This name must match what FastAPI calls
class DatasetPostUploadWF:
    @workflow.run
    async def run(self, seconds: int) -> str:
        print(f"[Workflow] Starting workflow with sleep={seconds}")
        result = await workflow.execute_activity(
            x_sleep,
            seconds,
            schedule_to_close_timeout=timedelta(minutes=30),
        )
        return result
