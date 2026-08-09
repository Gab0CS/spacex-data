from __future__ import annotations

import asyncio

from pydantic import BaseModel

from app.clients.spacex_client import SpaceXClientProtocol
from app.core.cache import TTLCache

_CACHE_KEY = "rockets"


class Distance(BaseModel):
    meters: float | None = None
    feet: float | None = None


class Mass(BaseModel):
    kg: float | None = None
    lb: float | None = None


class PayloadWeight(BaseModel):
    id: str
    name: str
    kg: float | None = None
    lb: float | None = None


class Thrust(BaseModel):
    kN: float | None = None
    lbf: float | None = None


class FirstStage(BaseModel):
    reusable: bool | None = None
    engines: int | None = None
    fuel_amount_tons: float | None = None
    burn_time_sec: int | None = None
    thrust_sea_level: Thrust | None = None
    thrust_vacuum: Thrust | None = None


class CompositeFairing(BaseModel):
    height: Distance | None = None
    diameter: Distance | None = None


class Payloads(BaseModel):
    option_1: str | None = None
    option_2: str | None = None
    composite_fairing: CompositeFairing | None = None


class SecondStage(BaseModel):
    engines: int | None = None
    fuel_amount_tons: float | None = None
    burn_time_sec: int | None = None
    thrust: Thrust | None = None
    payloads: Payloads | None = None


class Engines(BaseModel):
    number: int | None = None
    type: str | None = None
    version: str | None = None
    layout: str | None = None
    engine_loss_max: int | None = None
    propellant_1: str | None = None
    propellant_2: str | None = None
    thrust_sea_level: Thrust | None = None
    thrust_vacuum: Thrust | None = None
    thrust_to_weight: float | None = None


class LandingLegs(BaseModel):
    number: int | None = None
    material: str | None = None


class Rocket(BaseModel):
    id: int | str | None = None
    rocket_id: str
    rocket_name: str
    rocket_type: str | None = None
    active: bool = False
    stages: int = 0
    boosters: int = 0
    cost_per_launch: int | None = None
    success_rate_pct: float | None = None
    first_flight: str | None = None
    country: str | None = None
    company: str | None = None
    height: Distance | None = None
    diameter: Distance | None = None
    mass: Mass | None = None
    payload_weights: list[PayloadWeight] = []
    first_stage: FirstStage | None = None
    second_stage: SecondStage | None = None
    engines: Engines | None = None
    landing_legs: LandingLegs | None = None
    wikipedia: str | None = None
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
            **{
                **raw,
                "rocket_id": raw.get("rocket_id", raw.get("id")),
                "rocket_name": raw.get("rocket_name", raw.get("name")),
                "rocket_type": raw.get("rocket_type", raw.get("type")),
            }
        )
