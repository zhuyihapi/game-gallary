from fastapi import FastAPI, Request
from app.routers import game_router
from contextlib import asynccontextmanager
from starlette.responses import JSONResponse

from app.database.mysql import initialize_mysql, close_mysql


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_mysql()
    yield
    await close_mysql()


app = FastAPI(lifespan=lifespan)
app.include_router(game_router.router)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"code": 500, "message": f"internel error: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
