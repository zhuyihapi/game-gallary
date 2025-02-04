from fastapi import FastAPI
from app.routers import game_router
from contextlib import asynccontextmanager

from app.database.mysql import initialize_mysql, close_mysql


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_mysql()

    yield
    await close_mysql()


app.include_router(game_router.router)
