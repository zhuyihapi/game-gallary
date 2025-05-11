from pydantic import BaseModel
from typing import Any, Optional


class ResponseModel(BaseModel):
    code: int = 0
    msg: str = ""
    data: Optional[Any] = None
