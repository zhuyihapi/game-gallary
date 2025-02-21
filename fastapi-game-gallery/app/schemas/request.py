from pydantic import BaseModel
from typing import List
from datetime import datetime


class DateRequest(BaseModel):
    year_months: List[str]  # 期望格式如: ["2023-01", "2024-02"]

    # 添加验证
    class Config:
        schema_extra = {"example": {"year_months": ["2023-01", "2023-02", "2024-01"]}}

    @classmethod
    def validate_date_format(cls, values):
        """验证日期格式"""
        for ym in values.get("year_months", []):
            try:
                datetime.strptime(ym, "%Y-%m")
            except ValueError:
                raise ValueError(f"Invalid year-month format: {ym}. Expected YYYY-MM")
        return values
