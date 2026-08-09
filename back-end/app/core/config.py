from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    spacex_api_base_url: str = "https://api.spacexdata.com"
    spacex_api_timeout_seconds: float = 10.0
    cache_ttl_seconds: float = 900.0
    cache_refresh_interval_seconds: float = 300.0
    cors_origins: list[str] = ["*"]
    use_mock_data: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings(
        spacex_api_base_url=os.getenv("SPACEX_API_BASE_URL", "https://api.spacexdata.com"),
        spacex_api_timeout_seconds=float(os.getenv("SPACEX_API_TIMEOUT_SECONDS", "10")),
        cache_ttl_seconds=float(os.getenv("CACHE_TTL_SECONDS", "900")),
        cache_refresh_interval_seconds=float(os.getenv("CACHE_REFRESH_INTERVAL_SECONDS", "300")),
        cors_origins=os.getenv("CORS_ORIGINS", "*").split(","),
        use_mock_data=os.getenv("USE_MOCK_DATA", "false").lower() in ("1", "true", "yes"),
    )
