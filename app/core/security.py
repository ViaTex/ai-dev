from __future__ import annotations

from fastapi import Header

from app.core.config import get_settings
from app.utils.validators import InvalidAPIKeyError


async def verify_internal_api_key(x_internal_api_key: str = Header(..., alias="X-Internal-API-Key")) -> None:
    settings = get_settings()
    if x_internal_api_key != settings.internal_api_key:
        raise InvalidAPIKeyError("Invalid internal API key")
