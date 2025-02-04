import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

log_dir = BASE_DIR / "logs"
log_file_path = log_dir / "app.log"

log_dir.mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 创建文件处理器（按日期分割日志文件）
file_handler = TimedRotatingFileHandler(
    filename=str(log_file_path), when="midnight", interval=1, backupCount=7
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)  # 按需调整

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)  # 按需调整

# 创建全局日志记录器
logger = logging.getLogger("Chat BI - fast-nebula")
logger.setLevel(logging.DEBUG)  # 按需调整

# 防止重复添加处理器（检查是否已配置处理器）
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# 测试
if __name__ == "__main__":
    logger.debug("This is a DEBUG log")
    logger.info("This is an INFO log")
    logger.warning("This is a WARNING log")
    logger.error("This is an ERROR log")
    logger.critical("This is a CRITICAL log")
