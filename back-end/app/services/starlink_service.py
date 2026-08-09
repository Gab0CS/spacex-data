from __future__ import annotations

import asyncio

from pydantic import BaseModel

from app.clients.spacex_client import SpaceXClientProtocol
from app.core.cache import TTLCache

_CACHE_KEY = "starlink"


class StarlinkSatellite(BaseModel):
    id: str
    name: str | None = None
    version: str | None = None
    launch_id: str | None = None
    is_active: bool


class StarlinkService:
    def __init__(self, client: SpaceXClientProtocol, cache: TTLCache[list[StarlinkSatellite]]) -> None:
        self._client = client
        self._cache = cache
        self._lock = asyncio.Lock()

    async def get_satellites(self) -> list[StarlinkSatellite]:
        cached = self._cache.get(_CACHE_KEY)
        if cached is not None:
            return cached
        async with self._lock:
            cached = self._cache.get(_CACHE_KEY)
            if cached is not None:
                return cached
            return await self.refresh()

    async def refresh(self) -> list[StarlinkSatellite]:
        raw_satellites = await self._client.get_starlink()
        satellites = [self._to_satellite(raw) for raw in raw_satellites]
        self._cache.set(_CACHE_KEY, satellites)
        return satellites

    @staticmethod
    def _to_satellite(raw: dict) -> StarlinkSatellite:
        space_track = raw.get("spaceTrack") or {}
        return StarlinkSatellite(
            id=raw["id"],
            name=space_track.get("OBJECT_NAME"),
            version=raw.get("version"),
            launch_id=raw.get("launch"),
            is_active=space_track.get("DECAYED") == 0,
        )
