from app.config import (
    LOG_FILE_PATH,
    LOG_LEVEL,
    FILE_LOG_LEVEL,
    CONSOLE_LOG_LEVEL,
    LOG_NAME,
    ROOT_DIR
)
from loguru import logger
from pathlib import Path
import sys
import os


Path(LOG_FILE_PATH).parent.mkdir(parents=True, exist_ok=True)

logger.remove()

def format_record(record):
    level = record["level"].name

    # 定义颜色/样式嵌套的 map
    style_map = {
        "DEBUG": lambda text: f"<cyan>{text}</cyan>",
        "INFO": lambda text: f"<green>{text}</green>",
        "WARNING": lambda text: f"<yellow>{text}</yellow>",
        "ERROR": lambda text: f"<red>{text}</red>",
        "CRITICAL": lambda text: f"<red><bold><reverse>{text}</reverse></bold></red>",
    }

    style = style_map.get(level, lambda text: text)

    return (
        f"{record['time']:YYYY-MM-DD HH:mm:ss} - "
        f"{record['name']} - "
        f"{style(f'{level:<8}')} - "
        f"{record['message']}"
    )

# logger.level("DEBUG", color="<cyan>")
# logger.level("INFO", color="<green>")
# logger.level("WARNING", color="<yellow>")
# logger.level("ERROR", color="<red><bold>")
# logger.level("CRITICAL", color="<red><bold><reverse>")

logger.add(
    sys.stdout,
    level=CONSOLE_LOG_LEVEL,
    # format=format_record,
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

logger.add(
    LOG_FILE_PATH,
    level=FILE_LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} - {name} - {level} - {message}",
    rotation="10 MB",
    retention=20,
    encoding="utf-8",
    enqueue=True,
)

# 示例：loguru 不再需要 logger = logging.getLogger()，直接使用 logger 即可
if __name__ == "__main__":
    logger.debug("This is a DEBUG log")
    logger.info("This is an INFO log")
    logger.warning("This is a WARNING log")
    logger.error("This is an ERROR log")
    logger.critical("This is a CRITICAL log")
