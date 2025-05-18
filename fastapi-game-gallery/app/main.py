from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
from starlette.responses import JSONResponse
import uuid

from app.routers import game_router, manager_router
from app.database.mysql import initialize_mysql, close_mysql
from app.scheduler import start_scheduler, shutdown_scheduler
from app.logger import init_logger
from loguru import logger
from app.config import LOG_DIR, MODULE_NAME

LOG_FILE_PATH = f"{LOG_DIR}/{MODULE_NAME}_{{time:YYYY-MM-DD}}.log"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger(
        log_file_path=LOG_FILE_PATH,
        log_name=MODULE_NAME,
        console_level="INFO",
        file_level="DEBUG",
        rotation="00:00",
        retention=30,
    )
    initialize_mysql()
    await start_scheduler()
    yield
    await shutdown_scheduler()
    close_mysql()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    middleware: add ID to every requests
    """

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestIDMiddleware)
app.include_router(game_router.router)
app.include_router(manager_router.router)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"code": 500, "message": f"internel error: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
