from loguru import logger
from pathlib import Path
from contextvars import ContextVar

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="unknown")
# request_id_ctx.set("SYSTEM")  # default value for request ID

def _request_id_filter(record):
    record["extra"]["request_id"] = request_id_ctx.get()
    return True


def init_logger(
    log_file_path: str,
    log_name: str = "app_log",
    console_level: str = "INFO",
    file_level: str = "DEBUG",
    rotation: str = "00:00",
    retention: int = 30,
):
    import sys

    Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
    logger.remove()

    # 控制台
    logger.add(
        sys.stdout,
        level=console_level,
        enqueue=True,
        backtrace=True,
        diagnose=True,
        filter=_request_id_filter,
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {extra[request_id]} | {message}",
    )

    # 日志文件
    logger.add(
        log_file_path,
        level=file_level,
        rotation=rotation,
        retention=retention,
        encoding="utf-8",
        filter=_request_id_filter,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | [{module}] {message}",
    )

    logger.bind(request_id="logger_init").info(f"日志初始化完成，路径: {log_file_path}")


if __name__ == "__main__":
    logger.debug("This is a DEBUG log")
    logger.info("This is an INFO log")
    logger.warning("This is a WARNING log")
    logger.error("This is an ERROR log")
    logger.critical("This is a CRITICAL log")


# from loguru import logger
# from pathlib import Path
# import sys
# import os

# LOG_DIR.parent.mkdir(parents=True, exist_ok=True)
# LOG_FILE_PATH = f"{LOG_DIR}/{LOG_NAME}_{{time:YYYY-MM-DD}}.log"
# logger.remove()


# def format_record(record):
#     level = record["level"].name

#     # 定义颜色/样式嵌套的 map
#     style_map = {
#         "DEBUG": lambda text: f"<cyan>{text}</cyan>",
#         "INFO": lambda text: f"<green>{text}</green>",
#         "WARNING": lambda text: f"<yellow>{text}</yellow>",
#         "ERROR": lambda text: f"<red>{text}</red>",
#         "CRITICAL": lambda text: f"<red><bold><reverse>{text}</reverse></bold></red>",
#     }

#     style = style_map.get(level, lambda text: text)

#     return (
#         f"{record['time']:YYYY-MM-DD HH:mm:ss} - "
#         f"{record['name']} - "
#         f"{style(f'{level:<8}')} - "
#         f"{record['message']}"
#     )


# logger.add(
#     sys.stdout,
#     level=CONSOLE_LOG_LEVEL,
#     # format=format_record,
#     enqueue=True,
#     backtrace=True,
#     diagnose=True,
# )

# logger.add(
#     LOG_FILE_PATH,
#     level=FILE_LOG_LEVEL,
#     format="{time:YYYY-MM-DD HH:mm:ss} - {name} - {level} - {message}",
#     # rotation="10 MB",
#     rotation="00:00",
#     retention=30,
#     encoding="utf-8",
# )

# 示例：loguru 不再需要 logger = logging.getLogger()，直接使用 logger 即可
