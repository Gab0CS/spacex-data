from __future__ import annotations

import asyncio
from datetime import datetime

from pydantic import BaseModel

from app.clients.spacex_client import SpaceXClientProtocol
from app.core.cache import TTLCache

_CACHE_KEY = "launches"


class OrbitParams(BaseModel):
    reference_system: str | None = None
    regime: str | None = None
    longitude: float | None = None
    semi_major_axis_km: float | None = None
    eccentricity: float | None = None
    periapsis_km: float | None = None
    apoapsis_km: float | None = None
    inclination_deg: float | None = None
    period_min: float | None = None
    lifespan_years: float | None = None
    epoch: str | None = None
    mean_motion: float | None = None
    raan: float | None = None
    arg_of_pericenter: float | None = None
    mean_anomaly: float | None = None


class Payload(BaseModel):
    payload_id: str
    norad_id: list[int] = []
    reused: bool = False
    customers: list[str] = []
    nationality: str | None = None
    manufacturer: str | None = None
    payload_type: str | None = None
    payload_mass_kg: float | None = None
    payload_mass_lbs: float | None = None
    orbit: str | None = None
    orbit_params: OrbitParams | None = None


class Core(BaseModel):
    core_serial: str | None = None
    flight: int | None = None
    block: int | None = None
    gridfins: bool | None = None
    legs: bool | None = None
    reused: bool | None = None
    land_success: bool | None = None
    landing_intent: bool | None = None
    landing_type: str | None = None
    landing_vehicle: str | None = None


class FirstStageInfo(BaseModel):
    cores: list[Core] = []


class SecondStageInfo(BaseModel):
    block: int | None = None
    payloads: list[Payload] = []


class Fairings(BaseModel):
    reused: bool | None = None
    recovery_attempt: bool | None = None
    recovered: bool | None = None
    ship: str | None = None


class LaunchRocket(BaseModel):
    rocket_id: str
    rocket_name: str
    rocket_type: str | None = None
    first_stage: FirstStageInfo | None = None
    second_stage: SecondStageInfo | None = None
    fairings: Fairings | None = None


class LaunchSite(BaseModel):
    site_id: str | None = None
    site_name: str | None = None
    site_name_long: str | None = None


class LaunchLinks(BaseModel):
    mission_patch: str | None = None
    mission_patch_small: str | None = None
    reddit_campaign: str | None = None
    reddit_launch: str | None = None
    reddit_recovery: str | None = None
    reddit_media: str | None = None
    presskit: str | None = None
    article_link: str | None = None
    wikipedia: str | None = None
    video_link: str | None = None
    youtube_id: str | None = None
    flickr_images: list[str] = []


class LaunchFailureDetails(BaseModel):
    time: float | None = None
    altitude: float | None = None
    reason: str | None = None


class Telemetry(BaseModel):
    flight_club: str | None = None


class Launch(BaseModel):
    id: str
    flight_number: int
    mission_name: str
    mission_id: list[str] = []
    upcoming: bool
    launch_year: str | None = None
    launch_date_unix: int | None = None
    launch_date_utc: datetime
    launch_date_local: str | None = None
    is_tentative: bool = False
    tentative_max_precision: str | None = None
    tbd: bool = False
    launch_window: int | None = None
    rocket: LaunchRocket
    ships: list[str] = []
    telemetry: Telemetry | None = None
    launch_site: LaunchSite | None = None
    launch_success: bool | None = None
    launch_failure_details: LaunchFailureDetails | None = None
    links: LaunchLinks | None = None
    details: str | None = None
    static_fire_date_utc: datetime | None = None
    static_fire_date_unix: int | None = None
    timeline: dict[str, float | None] = {}


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
        if "flight_number" in raw:
            return Launch(**raw)

        rocket = raw.get("rocket")
        rocket_id = rocket if isinstance(rocket, str) else (rocket or {}).get("rocket_id", "unknown")
        return Launch(
            id=raw["id"],
            flight_number=raw.get("flight_number", 0),
            mission_name=raw["name"],
            upcoming=raw.get("upcoming", False),
            launch_date_utc=raw["date_utc"],
            rocket=LaunchRocket(rocket_id=rocket_id, rocket_name=rocket_id),
            launch_success=raw.get("success"),
            details=raw.get("details"),
            static_fire_date_utc=raw.get("static_fire_date_utc"),
        )
