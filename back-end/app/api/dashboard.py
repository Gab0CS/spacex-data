from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_dashboard_service
from app.services.dashboard_service import DashboardService, DashboardStats

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(
    dashboard_service: DashboardService = Depends(get_dashboard_service),
) -> DashboardStats:
    return await dashboard_service.get_dashboard_stats()
