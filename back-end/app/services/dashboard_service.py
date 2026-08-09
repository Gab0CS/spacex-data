from __future__ import annotations

import asyncio
from collections import Counter

from pydantic import BaseModel

from app.services.launch_service import LaunchService
from app.services.rocket_service import RocketService
from app.services.starlink_service import StarlinkService


class DashboardStats(BaseModel):
    total_rockets: int
    total_launches: int
    successful_launches: int
    failed_launches: int
    launch_success_rate: float
    active_starlink_satellites: int
    inactive_starlink_satellites: int
    launches_per_year: dict[int, int]


class DashboardService:
    def __init__(
        self,
        rocket_service: RocketService,
        launch_service: LaunchService,
        starlink_service: StarlinkService,
    ) -> None:
        self._rocket_service = rocket_service
        self._launch_service = launch_service
        self._starlink_service = starlink_service

    async def get_dashboard_stats(self) -> DashboardStats:
        rockets, launches, satellites = await asyncio.gather(
            self._rocket_service.get_rockets(),
            self._launch_service.get_launches(),
            self._starlink_service.get_satellites(),
        )

        decided_launches = [launch for launch in launches if launch.launch_success is not None]
        successful_launches = sum(1 for launch in decided_launches if launch.launch_success)
        failed_launches = len(decided_launches) - successful_launches
        success_rate = (successful_launches / len(decided_launches) * 100) if decided_launches else 0.0

        launches_per_year = Counter(launch.launch_date_utc.year for launch in launches)
        active_satellites = sum(1 for satellite in satellites if satellite.is_active)

        return DashboardStats(
            total_rockets=len(rockets),
            total_launches=len(launches),
            successful_launches=successful_launches,
            failed_launches=failed_launches,
            launch_success_rate=round(success_rate, 2),
            active_starlink_satellites=active_satellites,
            inactive_starlink_satellites=len(satellites) - active_satellites,
            launches_per_year=dict(sorted(launches_per_year.items())),
        )
