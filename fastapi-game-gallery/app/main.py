from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from starlette.responses import JSONResponse
from app.routers import game_router
from app.database.mysql import initialize_mysql, close_mysql
from app.scheduler import start_scheduler, shutdown_scheduler
from app.logger import init_logger
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
    start_scheduler()

    yield
    shutdown_scheduler()
    close_mysql()


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
