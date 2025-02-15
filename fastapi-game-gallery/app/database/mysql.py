from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import mysql_settings_dev, session_maker_settings_dev
from app.log.logger import logger


_engine = None
_SessionMaker = None


async def initialize_mysql() -> None:
    """初始化MySQL数据库连接池"""
    logger.debug("Initializing MySQL connection...")
    global _engine, _SessionMaker
    try:
        # aiomysql or asyncmy
        database_url = f"mysql+asyncmy://{mysql_settings_dev.MYSQL_USER}:{mysql_settings_dev.MYSQL_PASSWORD}@{mysql_settings_dev.MYSQL_HOST}:{mysql_settings_dev.MYSQL_PORT}/{mysql_settings_dev.MYSQL_DATABASE}"
        # logger.debug("database_url is %s", database_url)
        _engine = create_async_engine(
            database_url,
            echo=mysql_settings_dev.ECHO,
            pool_size=mysql_settings_dev.POOL_SIZE,
            max_overflow=mysql_settings_dev.MAX_OVERFLOW,
            future=mysql_settings_dev.FUTURE,
        )
        _SessionMaker = async_sessionmaker(
            bind=_engine,
            class_=AsyncSession,
            expire_on_commit=session_maker_settings_dev.expired_on_commit,
        )
        async with _engine.begin() as conn:
            # logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
            # 可选：测试连接
            await conn.execute(text("SELECT 1"))
        logger.info(f"MySQL connection initialized at {mysql_settings_dev.MYSQL_HOST}.")
    except SQLAlchemyError as e:
        logger.error(f"Failed to initialize MySQL: {e}")
        raise


Base = declarative_base()


async def initialize_tables() -> None:
    """初始化数据库表"""
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_mysql_session() -> AsyncGenerator[AsyncSession, None]:
    """获取MySQL数据库Session"""
    global _SessionMaker
    if _SessionMaker is None:
        raise RuntimeError("MySQL session maker is not initialized.")
    async with _SessionMaker() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error(f"MySQL session error: {e}")
            raise
        finally:
            await session.close()


async def close_mysql() -> None:
    """关闭MySQL数据库连接池"""
    global _engine
    if _engine:
        await _engine.dispose()
        logger.info("MySQL connection pool successfully closed.")
    else:
        logger.warning("Attempted to close MySQL, but no engine was initialized.")
