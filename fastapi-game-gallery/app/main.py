from fastapi import FastAPI
from app.routers import game_router
from contextlib import asynccontextmanager

from app.database.mysql import initialize_mysql, close_mysql


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_mysql()
    yield
    await close_mysql()


app = FastAPI(lifespan=lifespan)
app.include_router(game_router.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
