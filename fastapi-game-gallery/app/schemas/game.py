from pydantic import BaseModel
from typing import List, Optional

class Game(BaseModel):
    id: int
    title: str
    release_date: Optional[str] = None
    platforms: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    image_url: Optional[str] = None
    anticipation_rating: Optional[int] = None
    description: Optional[str] = None