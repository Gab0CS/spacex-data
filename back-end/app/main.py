from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import dashboard, rockets, starlink
from app.clients.mock_spacex_client import MockSpaceXClient
from app.clients.spacex_client import SpaceXClient, SpaceXClientProtocol
from app.core.cache import TTLCache
from app.core.config import get_settings
from app.core.exceptions import SpaceXAPIError
from app.core.scheduler import CacheRefreshScheduler
from app.services.dashboard_service import DashboardService
from app.services.launch_service import LaunchService
from app.services.rocket_service import RocketService
from app.services.starlink_service import StarlinkService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    client: SpaceXClientProtocol
    if settings.use_mock_data:
        logger.warning("USE_MOCK_DATA is enabled, serving canned SpaceX data instead of live API calls")
        client = MockSpaceXClient()
    else:
        client = SpaceXClient(settings.spacex_api_base_url, settings.spacex_api_timeout_seconds)

    rocket_service = RocketService(client, TTLCache(settings.cache_ttl_seconds))
    launch_service = LaunchService(client, TTLCache(settings.cache_ttl_seconds))
    starlink_service = StarlinkService(client, TTLCache(settings.cache_ttl_seconds))
    dashboard_service = DashboardService(rocket_service, launch_service, starlink_service)

    app.state.rocket_service = rocket_service
    app.state.launch_service = launch_service
    app.state.starlink_service = starlink_service
    app.state.dashboard_service = dashboard_service

    for name, service in (
        ("rockets", rocket_service),
        ("launches", launch_service),
        ("starlink", starlink_service),
    ):
        try:
            await service.refresh()
        except SpaceXAPIError:
            logger.warning("Initial %s cache warm-up failed, will retry on first request", name)

    scheduler = CacheRefreshScheduler(
        rocket_service,
        launch_service,
        starlink_service,
        settings.cache_refresh_interval_seconds,
    )
    scheduler.start()

    yield

    scheduler.shutdown()
    await client.aclose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="SpaceX Dashboard API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(dashboard.router)
    app.include_router(rockets.router)
    app.include_router(starlink.router)

    @app.exception_handler(SpaceXAPIError)
    async def handle_spacex_api_error(request, exc: SpaceXAPIError) -> JSONResponse:
        return JSONResponse(status_code=503, content={"detail": str(exc)})

    return app


app = create_app()
