from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from app.schemas.game import Game
from app.schemas.request import DateRequest
from app.service.temp import get_data_by_year_months

router = APIRouter()

@router.post("/get-by-dates")
async def get_data_by_dates(request: DateRequest):
    """
    根据多个年月获取数据
    Args:
        request: 包含年月列表的请求体
    Returns:
        dict: 服务层返回的数据
    Raises:
        HTTPException: 如果请求参数无效或服务层出错
    """

    DateRequest.validate_date_format({"year_months": request.year_months})
    
    result = await get_data_by_year_months(request.year_months)
    
    return {
        "status": "success",
        "data": result,
        "requested_dates": request.year_months
    }