from __future__ import annotations

import asyncio

from pydantic import BaseModel

from app.clients.spacex_client import SpaceXClientProtocol
from app.core.cache import TTLCache

_CACHE_KEY = "starlink"


class SpaceTrack(BaseModel):
    CCSDS_OMM_VERS: str | None = None
    COMMENT: str | None = None
    CREATION_DATE: str | None = None
    ORIGINATOR: str | None = None
    OBJECT_NAME: str | None = None
    OBJECT_ID: str | None = None
    CENTER_NAME: str | None = None
    REF_FRAME: str | None = None
    TIME_SYSTEM: str | None = None
    MEAN_ELEMENT_THEORY: str | None = None
    EPOCH: str | None = None
    MEAN_MOTION: float | None = None
    ECCENTRICITY: float | None = None
    INCLINATION: float | None = None
    RA_OF_ASC_NODE: float | None = None
    ARG_OF_PERICENTER: float | None = None
    MEAN_ANOMALY: float | None = None
    EPHEMERIS_TYPE: int | None = None
    CLASSIFICATION_TYPE: str | None = None
    NORAD_CAT_ID: int | None = None
    ELEMENT_SET_NO: int | None = None
    REV_AT_EPOCH: int | None = None
    BSTAR: float | None = None
    MEAN_MOTION_DOT: float | None = None
    MEAN_MOTION_DDOT: float | None = None
    SEMIMAJOR_AXIS: float | None = None
    PERIOD: float | None = None
    APOAPSIS: float | None = None
    PERIAPSIS: float | None = None
    OBJECT_TYPE: str | None = None
    RCS_SIZE: str | None = None
    COUNTRY_CODE: str | None = None
    LAUNCH_DATE: str | None = None
    SITE: str | None = None
    DECAY_DATE: str | None = None
    DECAYED: int | None = None
    FILE: int | None = None
    GP_ID: int | None = None
    TLE_LINE0: str | None = None
    TLE_LINE1: str | None = None
    TLE_LINE2: str | None = None


class StarlinkSatellite(BaseModel):
    id: str
    version: str | None = None
    launch: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    height_km: float | None = None
    velocity_kms: float | None = None
    spaceTrack: SpaceTrack | None = None
    is_active: bool = False


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
            **{
                **raw,
                "is_active": space_track.get("DECAYED") == 0,
            }
        )
