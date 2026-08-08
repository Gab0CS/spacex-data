from __future__ import annotations

import httpx

from app.core.exceptions import SpaceXAPIError


class SpaceXClient:
    def __init__(self, base_url: str, timeout_seconds: float) -> None:
        self._http = httpx.AsyncClient(base_url=base_url, timeout=timeout_seconds)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def get_rockets(self) -> list[dict]:
        return await self._get("/v4/rockets")

    async def get_launches(self) -> list[dict]:
        return await self._get("/v5/launches")

    async def get_starlink(self) -> list[dict]:
        return await self._get("/v4/starlink")

    async def _get(self, path: str) -> list[dict]:
        try:
            response = await self._http.get(path)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SpaceXAPIError(f"Request to SpaceX API failed: {path}") from exc
        return response.json()
