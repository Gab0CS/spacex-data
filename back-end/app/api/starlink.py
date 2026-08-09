from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_starlink_service
from app.services.starlink_service import StarlinkSatellite, StarlinkService

router = APIRouter(prefix="/api", tags=["starlink"])


@router.get("/starlink", response_model=list[StarlinkSatellite])
async def list_starlink(
    starlink_service: StarlinkService = Depends(get_starlink_service),
) -> list[StarlinkSatellite]:
    return await starlink_service.get_satellites()
