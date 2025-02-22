import datetime
from sqlalchemy import text, MetaData, Connection, Engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger
from app.database.game_model import Base

def check_and_update_table(conn: Connection, _engine: Engine) -> None:
    """Check if the `game_release` table structure matches, archive the old table and recreate if not"""
    try:
        logger.debug("Checking `game_release` table structure...")
        metadata = MetaData()
        metadata.reflect(bind=_engine)  # Refresh database structure

        if "game_release" not in metadata.tables:
            logger.warning("Table `game_release` does not exist, creating...")
            create_game_release_table(_engine)
        else:
            existing_table = metadata.tables["game_release"]

            expected_columns = {
                "id", "steam_id", "name", "release_date", "release_year",
                "release_quarter", "release_status"
            }
            existing_columns = {col.name for col in existing_table.columns}

            if expected_columns != existing_columns:
                logger.warning(
                    "`game_release` table structure does not match, archiving old table and recreating..."
                )
                archive_and_recreate_table(conn, _engine)
            else:
                logger.info("`game_release` table structure is correct, no update needed.")
    except SQLAlchemyError as e:
        logger.error(f"Database error while checking `game_release` table: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while checking `game_release` table: {e}")
        raise

def create_game_release_table(_engine: Engine) -> None:
    """Create only the `game_release` table"""
    try:
        from app.database.game_model import GameRelease
        
        logger.info(f"Ensuring table `game_release` is created...")
        GameRelease.__table__.create(bind=_engine, checkfirst=True)  # 目前仅创建 `game_release`
        logger.info("`game_release` table has been successfully created.")
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating `game_release` table: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while creating `game_release` table: {e}")
        raise

def archive_and_recreate_table(conn: Connection, _engine: Engine) -> None:
    """Archive the `game_release` table and recreate it"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        archived_table_name = f"game_release_backup_{timestamp}"

        # Rename the old table
        conn.execute(text(f"RENAME TABLE game_release TO {archived_table_name}"))
        conn.commit()
        logger.info(f"Old table has been archived as {archived_table_name}")

        # Recreate the new table
        create_game_release_table(_engine)
    except SQLAlchemyError as e:
        logger.error(f"Database error while archiving and recreating `game_release` table: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while archiving and recreating `game_release` table: {e}")
        raise
