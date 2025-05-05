from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from loguru import logger

from app.config import api_keys

router = APIRouter()

ADMIN_API_KEY = api_keys.ADMIN_API_KEY
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def verify_api_key(key: str = Depends(api_key_header)):
    if key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing X-API-KEY header",
        )


@router.post("/wishlist/update", dependencies=[Depends(verify_api_key)])
async def update_wishlist(request):
    pass
