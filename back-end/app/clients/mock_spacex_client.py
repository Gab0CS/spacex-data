from __future__ import annotations

from app.clients.mock_launches_data import MOCK_LAUNCHES
from app.clients.mock_rockets_data import MOCK_ROCKETS
from app.clients.mock_starlink_data import MOCK_STARLINK


class MockSpaceXClient:
    async def get_rockets(self) -> list[dict]:
        return MOCK_ROCKETS

    async def get_launches(self) -> list[dict]:
        return MOCK_LAUNCHES

    async def get_starlink(self) -> list[dict]:
        return MOCK_STARLINK

    async def aclose(self) -> None:
        return None
