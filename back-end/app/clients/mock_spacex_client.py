from __future__ import annotations

import asyncio
import random

from app.clients.mock_launches_data import MOCK_LAUNCHES
from app.clients.mock_rockets_data import MOCK_ROCKETS
from app.clients.mock_starlink_data import MOCK_STARLINK


class MockSpaceXClient:
    async def get_rockets(self) -> list[dict]:
        await self._simulate_latency()
        return MOCK_ROCKETS

    async def get_launches(self) -> list[dict]:
        await self._simulate_latency()
        return MOCK_LAUNCHES

    async def get_starlink(self) -> list[dict]:
        await self._simulate_latency()
        return MOCK_STARLINK

    async def aclose(self) -> None:
        return None

    @staticmethod
    async def _simulate_latency() -> None:
        await asyncio.sleep(random.uniform(1, 5))
