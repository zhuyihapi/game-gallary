# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import SQLAlchemyError

# from app.config import sqlite_settings, session_maker_settings_dev  # 配置文件中需包含 SQLITE_DB_PATH 等配置
# from app.logger import logger
# from app.database.sqlite_tables_init import check_and_update_table  # 请实现或调整该模块，负责建表或更新表结构

# _engine = None
# _SessionMaker = None


# def initialize_sqlite() -> None:
#     """初始化SQLite数据库连接池"""
#     logger.debug("Initializing SQLite connection...")
#     global _engine, _SessionMaker
#     try:
#         # 构造SQLite数据库URL（本地文件方式）
#         database_url = f"sqlite:///{sqlite_settings.SQLITE_DB_PATH}"
#         _engine = create_engine(
#             database_url,
#             connect_args={"check_same_thread": False}  # SQLite 多线程支持需要设置此参数
#         )
#         _SessionMaker = sessionmaker(
#             bind=_engine,
#             expire_on_commit=session_maker_settings_dev.expired_on_commit,
#             autocommit=False,
#             autoflush=False,
#         )

#         # 测试数据库连接
#         with _engine.connect() as conn:
#             conn.execute(text("SELECT 1"))
#             logger.debug("SQLite connection test successful.")

#         # 检查并更新数据表结构（如果需要）
#         with _engine.connect() as conn:
#             check_and_update_table(conn, _engine)
#             logger.info("SQLite table check completed.")

#         logger.info(f"SQLite connection initialized with database at `{sqlite_settings.SQLITE_DB_PATH}`.")
#     except SQLAlchemyError as e:
#         logger.error(f"Failed to initialize SQLite: {e}")
#         raise


# def get_sqlite_session():
#     """获取SQLite数据库Session，适用于FastAPI依赖注入"""
#     global _SessionMaker
#     if _SessionMaker is None:
#         raise RuntimeError("SQLite session maker is not initialized.")
#     session = _SessionMaker()
#     try:
#         yield session
#     except SQLAlchemyError as e:
#         logger.error(f"SQLite session error: {e}")
#         raise
#     finally:
#         session.close()


# def close_sqlite() -> None:
#     """关闭SQLite数据库连接池"""
#     global _engine
#     if _engine:
#         _engine.dispose()
#         logger.info("SQLite connection pool successfully closed.")
#     else:
#         logger.warning("Attempted to close SQLite, but no engine was initialized.")
