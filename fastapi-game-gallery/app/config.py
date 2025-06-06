from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path


# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent
env_path = ROOT_DIR / ".env"

if not env_path.exists():
    raise FileNotFoundError("`.env` 文件不存在！请先创建 `.env` 并正确配置环境变量。")


load_dotenv(dotenv_path=env_path)

class APIKeys(BaseSettings):
    ADMIN_API_KEY: str

    class Config:
        env_file = env_path
        env_file_encoding = "utf-8"
        extra = "ignore"

class BaseMysqlSettings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    class Config:
        env_file = env_path  # 让 pydantic 读取 .env
        env_file_encoding = "utf-8"
        extra = "ignore"


class DevMysqlSettings(BaseMysqlSettings):
    ECHO: bool = True
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    FUTURE: bool = True


class DevSessionMaker:
    expired_on_commit: bool = True


# class BaseSqliteSettings(BaseSettings):
#     SQLITE_DB_PATH: str

#     class Config:
#         env_file = env_path
#         env_file_encoding = "utf-8"
#         extra = "ignore"

# sqlite_settings_dev = BaseSqliteSettings()
mysql_settings_dev = DevMysqlSettings()
session_maker_settings_dev = DevSessionMaker()
api_keys = APIKeys()
# print(f"MYSQL_USER from MySQLSettings: {mysql_settings_dev.MYSQL_HOST}")
# print(f"MYSQL_USER from os.getenv: {os.getenv('MYSQL_HOST')}")


# 日志配置
# 日志目录
LOG_DIR = ROOT_DIR / "logs"

# 创建日志目录（如果不存在）
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)

# 模块名称
MODULE_NAME = "game-gallery"


# Twitch API 认证信息
# class TwitchSettings(BaseSettings):
#     TWITCH_CLIENT_ID: str
#     TWITCH_CLIENT_SECRET: str
#     TWITCH_ACCESS_TOKEN: str

#     class Config:
#         env_file = env_path
#         env_file_encoding = "utf-8"
#         extra = "ignore"


# twitch_settings = TwitchSettings()
# print(f"TWITCH_CLIENT_ID from TwitchSettings: {twitch_settings.TWITCH_CLIENT_ID}")
