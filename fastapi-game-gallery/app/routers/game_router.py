from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from app.schemas.game import Game


router = APIRouter()

# Sample data
games = [
    Game(id=1, title="Game One", release_date="2023-01-01", platforms=["PC", "PS5"], genres=["Action"], image_url="http://example.com/game1.jpg", anticipation_rating=8, description="An exciting action game."),
    Game(id=2, title="Game Two", release_date="2023-02-01", platforms=["Xbox", "PC"], genres=["Adventure"], image_url="http://example.com/game2.jpg", anticipation_rating=9, description="An adventurous journey."),
]

@router.get("/games", response_model=List[Game])
def get_games():
    return games

@router.get("/games/{game_id}", response_model=Game)
def get_game(game_id: int):
    for game in games:
        if game.id == game_id:
            return game
    return {"error": "Game not found"}