from __future__ import annotations

import asyncio

from pydantic import BaseModel

from app.clients.spacex_client import SpaceXClientProtocol
from app.core.cache import TTLCache

_CACHE_KEY = "rockets"


class Rocket(BaseModel):
    id: str
    name: str
    active: bool
    stages: int
    boosters: int
    success_rate_pct: float | None = None
    first_flight: str | None = None
    country: str | None = None
    description: str | None = None


class RocketService:
    def __init__(self, client: SpaceXClientProtocol, cache: TTLCache[list[Rocket]]) -> None:
        self._client = client
        self._cache = cache
        self._lock = asyncio.Lock()

    async def get_rockets(self) -> list[Rocket]:
        cached = self._cache.get(_CACHE_KEY)
        if cached is not None:
            return cached
        async with self._lock:
            cached = self._cache.get(_CACHE_KEY)
            if cached is not None:
                return cached
            return await self.refresh()

    async def refresh(self) -> list[Rocket]:
        raw_rockets = await self._client.get_rockets()
        rockets = [self._to_rocket(raw) for raw in raw_rockets]
        self._cache.set(_CACHE_KEY, rockets)
        return rockets

    @staticmethod
    def _to_rocket(raw: dict) -> Rocket:
        return Rocket(
            id=raw["id"],
            name=raw["name"],
            active=raw.get("active", False),
            stages=raw.get("stages", 0),
            boosters=raw.get("boosters", 0),
            success_rate_pct=raw.get("success_rate_pct"),
            first_flight=raw.get("first_flight"),
            country=raw.get("country"),
            description=raw.get("description"),
        )
