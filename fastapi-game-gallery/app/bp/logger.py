from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from loguru import logger

from app.config import (
    LOG_FILE_PATH,
    LOG_LEVEL,
    FILE_LOG_LEVEL,
    CONSOLE_LOG_LEVEL,
    LOG_NAME,
)

import logging
import colorlog

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 定义颜色格式化器
color_formatter = colorlog.ColoredFormatter(
    "%(asctime)s - %(name)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    reset=True,
)

# 普通文件日志格式
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 创建文件日志处理器（按日期切分日志文件）
# file_handler = TimedRotatingFileHandler(
#     filename=str(LOG_FILE_PATH), when="midnight", interval=1, backupCount=7, encoding="utf-8"
# )
file_handler = RotatingFileHandler(
    filename=str(LOG_FILE_PATH), maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
file_handler.setFormatter(file_formatter)
file_handler.setLevel(FILE_LOG_LEVEL)

# 创建控制台日志处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(color_formatter)
console_handler.setLevel(CONSOLE_LOG_LEVEL)

# 创建全局日志记录器
logger = logging.getLogger(LOG_NAME)
logger.setLevel(LOG_LEVEL)

# 防止重复添加处理器
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# 测试日志
if __name__ == "__main__":
    logger.debug("This is a DEBUG log")
    logger.info("This is an INFO log")
    logger.warning("This is a WARNING log")
    logger.error("This is an ERROR log")
    logger.critical("This is a CRITICAL log")
