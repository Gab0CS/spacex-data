from __future__ import annotations

from fastapi import Request

from app.services.dashboard_service import DashboardService
from app.services.launch_service import LaunchService
from app.services.rocket_service import RocketService
from app.services.starlink_service import StarlinkService


def get_rocket_service(request: Request) -> RocketService:
    return request.app.state.rocket_service


def get_launch_service(request: Request) -> LaunchService:
    return request.app.state.launch_service


def get_starlink_service(request: Request) -> StarlinkService:
    return request.app.state.starlink_service


def get_dashboard_service(request: Request) -> DashboardService:
    return request.app.state.dashboard_service
