from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_launch_service
from app.services.launch_service import Launch, LaunchService

router = APIRouter(prefix="/api", tags=["launches"])


@router.get("/launches", response_model=list[Launch])
async def list_launches(
    launch_service: LaunchService = Depends(get_launch_service),
) -> list[Launch]:
    return await launch_service.get_launches()
