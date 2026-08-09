from __future__ import annotations

import asyncio
from datetime import datetime

from pydantic import BaseModel

from app.clients.spacex_client import SpaceXClientProtocol
from app.core.cache import TTLCache

_CACHE_KEY = "launches"


class Launch(BaseModel):
    id: str
    name: str
    rocket_id: str | None = None
    date_utc: datetime
    success: bool | None = None
    upcoming: bool


class LaunchService:
    def __init__(self, client: SpaceXClientProtocol, cache: TTLCache[list[Launch]]) -> None:
        self._client = client
        self._cache = cache
        self._lock = asyncio.Lock()

    async def get_launches(self) -> list[Launch]:
        cached = self._cache.get(_CACHE_KEY)
        if cached is not None:
            return cached
        async with self._lock:
            cached = self._cache.get(_CACHE_KEY)
            if cached is not None:
                return cached
            return await self.refresh()

    async def refresh(self) -> list[Launch]:
        raw_launches = await self._client.get_launches()
        launches = [self._to_launch(raw) for raw in raw_launches]
        self._cache.set(_CACHE_KEY, launches)
        return launches

    @staticmethod
    def _to_launch(raw: dict) -> Launch:
        return Launch(
            id=raw["id"],
            name=raw["name"],
            rocket_id=raw.get("rocket"),
            date_utc=raw["date_utc"],
            success=raw.get("success"),
            upcoming=raw.get("upcoming", False),
        )
