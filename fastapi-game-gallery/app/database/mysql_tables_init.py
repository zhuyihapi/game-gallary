import datetime
from sqlalchemy import inspect, text, MetaData, Table, Connection, Engine
from sqlalchemy.ext.declarative import DeclarativeMeta

from app.logger import logger
from app.database.game_model import Base


def check_and_update_table(
    conn: Connection, _engine: Engine
) -> None:
    """Check if the `game_release` table structure matches, archive the old table and recreate if not"""
    logger.debug("Checking `game_release` table structure...")

    metadata = MetaData()
    metadata.reflect(bind=_engine)  # 强制刷新数据库结构

    if "game_release" not in metadata.tables:
        logger.warning("Table `game_release` does not exist, creating...")
        create_game_release_table(_engine)
    else:
        existing_table = metadata.tables["game_release"]

        expected_columns = {
            "id",
            "steam_id",
            "name",
            "release_date",
            "release_year",
            "release_quarter",
            "release_status",
        }
        existing_columns = {col.name for col in existing_table.columns}

        if expected_columns != existing_columns:
            logger.warning(
                "`game_release` table structure does not match, archiving old table and recreating..."
            )
            archive_and_recreate_table(conn, _engine, Base)
        else:
            logger.info("`game_release` table structure is correct, no update needed.")


def create_game_release_table(_engine: Engine) -> None:
    """Create the `game_release` table"""
    logger.info(f"Registered tables: {Base.metadata.tables.keys()}")
    Base.metadata.create_all(bind=_engine)
    logger.info("`game_release` table has been successfully created.")


def archive_and_recreate_table(
    conn: Connection, _engine: Engine, Base: DeclarativeMeta
) -> None:
    """Archive the `game_release` table and recreate it"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    archived_table_name = f"game_release_backup_{timestamp}"

    # Rename the old table (确保不在事务中执行)
    conn.execute(text(f"RENAME TABLE game_release TO {archived_table_name}"))
    conn.commit()  # 确保更改立即生效
    logger.info(f"Old table has been archived as {archived_table_name}")

    # Recreate the new table
    create_game_release_table(_engine, Base)
