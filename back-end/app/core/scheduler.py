from __future__ import annotations

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.launch_service import LaunchService
from app.services.rocket_service import RocketService
from app.services.starlink_service import StarlinkService

logger = logging.getLogger(__name__)


class CacheRefreshScheduler:
    def __init__(
        self,
        rocket_service: RocketService,
        launch_service: LaunchService,
        starlink_service: StarlinkService,
        interval_seconds: float,
    ) -> None:
        self._rocket_service = rocket_service
        self._launch_service = launch_service
        self._starlink_service = starlink_service
        self._scheduler = AsyncIOScheduler()
        self._interval_seconds = interval_seconds

    def start(self) -> None:
        self._scheduler.add_job(
            self._refresh_all,
            "interval",
            seconds=self._interval_seconds,
            id="refresh_spacex_cache",
        )
        self._scheduler.start()

    def shutdown(self) -> None:
        self._scheduler.shutdown(wait=False)

    async def _refresh_all(self) -> None:
        for name, service in (
            ("rockets", self._rocket_service),
            ("launches", self._launch_service),
            ("starlink", self._starlink_service),
        ):
            try:
                await service.refresh()
            except Exception:
                logger.exception("Failed to refresh %s cache", name)
