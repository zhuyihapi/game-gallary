from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.config import api_keys
from app.scheduler import update_steam_cache, update_popular_wishlist

router = APIRouter()

ADMIN_API_KEY = api_keys.ADMIN_API_KEY
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def verify_admin_key(key: str = Depends(api_key_header)):
    if key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing X-API-KEY header",
        )


@router.post("/wishlist/update", dependencies=[Depends(verify_admin_key)])
async def update_wishlist(request):
    await update_steam_cache()
    result = await update_popular_wishlist()
    return {
        "status": "success",
        "message": f"Wishlist updated successfully, count: {result}",
    }
