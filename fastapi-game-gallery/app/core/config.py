import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载 .env 文件
if not os.path.exists(".env"):
    raise FileNotFoundError("❌ `.env` 文件不存在！请先复制 `.env.example` 并正确配置环境变量。")
load_dotenv()

class BaseMysqlSettings(BaseSettings):
    HOST: str = os.getenv("MYSQL_HOST")
    PORT: int = int(os.getenv("MYSQL_PORT", 3306))
    USER: str = os.getenv("MYSQL_USER")
    PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    DATABASE: str = os.getenv("MYSQL_DATABASE")

class DevMysqlSettings(BaseMysqlSettings):
    ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"
    POOL_SIZE: int = int(os.getenv("SQLALCHEMY_POOL_SIZE", 5))
    MAX_OVERFLOW: int = int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", 10))
    FUTURE: bool = os.getenv("SQLALCHEMY_FUTURE", "True").lower() == "true"

class DevSessionMaker:
    expired_on_commit: bool = True

mysql_settings_dev = DevMysqlSettings()
session_maker_settings_dev = DevSessionMaker()
