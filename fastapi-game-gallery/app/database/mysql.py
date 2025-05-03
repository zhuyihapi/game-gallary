from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from app.config import mysql_settings_dev, session_maker_settings_dev
from app.database.mysql_tables_init import check_and_update_table

_engine = None
_SessionMaker = None


def initialize_mysql() -> None:
    """初始化MySQL数据库连接池"""
    logger.debug("Initializing MySQL connection...")
    global _engine, _SessionMaker
    try:
        # 同步数据库连接
        database_url = f"mysql+pymysql://{mysql_settings_dev.MYSQL_USER}:{mysql_settings_dev.MYSQL_PASSWORD}@{mysql_settings_dev.MYSQL_HOST}:{mysql_settings_dev.MYSQL_PORT}/{mysql_settings_dev.MYSQL_DATABASE}"
        _engine = create_engine(
            database_url,
            echo=mysql_settings_dev.ECHO,
            pool_size=mysql_settings_dev.POOL_SIZE,
            max_overflow=mysql_settings_dev.MAX_OVERFLOW,
            future=mysql_settings_dev.FUTURE,
        )
        _SessionMaker = sessionmaker(
            bind=_engine, expire_on_commit=session_maker_settings_dev.expired_on_commit
        )

        # 测试数据库连接
        with _engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.debug("MySQL connection test successful.")

        with _engine.connect() as conn:
            check_and_update_table(conn, _engine)
            logger.info("MySQL table check completed.")

        logger.info(
            f"MySQL connection initialized at {mysql_settings_dev.MYSQL_HOST} with database `{mysql_settings_dev.MYSQL_DATABASE}`."
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to initialize MySQL: {e}")
        raise


# def initialize_tables() -> None:
#     """初始化数据库表"""
#     with _engine.begin() as conn:
#         Base.metadata.create_all(bind=conn)


def get_mysql_session():
    """获取MySQL数据库Session"""
    global _SessionMaker
    if _SessionMaker is None:
        raise RuntimeError("MySQL session maker is not initialized.")
    session = _SessionMaker()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.error(f"MySQL session error: {e}")
        raise
    finally:
        session.close()


def close_mysql() -> None:
    """关闭MySQL数据库连接池"""
    global _engine
    if _engine:
        _engine.dispose()
        logger.info("MySQL connection pool successfully closed.")
    else:
        logger.warning("Attempted to close MySQL, but no engine was initialized.")
