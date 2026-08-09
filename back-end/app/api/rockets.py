from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_rocket_service
from app.services.rocket_service import Rocket, RocketService

router = APIRouter(prefix="/api", tags=["rockets"])


@router.get("/rockets", response_model=list[Rocket])
async def list_rockets(
    rocket_service: RocketService = Depends(get_rocket_service),
) -> list[Rocket]:
    return await rocket_service.get_rockets()
