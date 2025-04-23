import asyncio

from temporalio.client import Client as TemporalClient

from src.core.config import settings


class TemporalClientProvider:
    def __init__(self):
        self._client: TemporalClient | None = None
        self._lock = asyncio.Lock()

    async def get(self) -> TemporalClient:
        async with self._lock:
            if not self._client:
                self._client = await TemporalClient.connect(settings.TEMPORAL_ADDRESS)
            return self._client


temporal_client_provider = TemporalClientProvider()


async def get_temporal_client() -> TemporalClient:
    return await temporal_client_provider.get()
