from fastapi import Depends
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from loguru import logger
import time
import aiohttp
import pandas as pd

from app.api.steam_store_match import fetch_steam_app_list
from app.database.mysql import get_mysql_session
from app.api.fetch_from_wishlist import (
    temp_save_to_mysql,
    get_popular_wishlist,
    parse_popular_wishlist,
)

scheduler = AsyncIOScheduler()


def update_steam_cache():
    # logger.info(f"[{datetime.now()}] 正在更新 Steam App 缓存...")
    data = fetch_steam_app_list()
    if data:
        logger.info(
            f"[{datetime.now()}] Steam App 缓存更新完成（共 {len(data['applist']['apps'])} 个应用）"
        )
    else:
        logger.info(f"[{datetime.now()}] Steam App 缓存更新失败")


def update_popular_wishlist(session: Session = Depends(get_mysql_session)):
    logger.info(f"开始更新 popular_wishlist 数据...")
    try:
        file1 = get_popular_wishlist(0, 50)
        time.sleep(5)
        file2 = get_popular_wishlist(50, 50)

        df1 = parse_popular_wishlist(file_path=file1)
        df2 = parse_popular_wishlist(file_path=file2)
        df = pd.concat([df1, df2], ignore_index=True)

        if df.empty:
            logger.warning("解析结果为空，未获取到任何热门愿望单数据。")
            return

        temp_save_to_mysql(df, session)
        session.commit()
        logger.info(
            f"[{datetime.now()}] popular_wishlist 数据更新完成，共保存 {len(df)} 条记录。"
        )
    except Exception as e:
        session.rollback()
        logger.error(f"更新 popular_wishlist 数据失败: {e}")


def update_popular_wishlist_wrapper():
    """
    包装函数：手动获取 Session 后调用 update_popular_wishlist。
    APScheduler 执行任务时无法自动解析 FastAPI 的依赖注入，所以需要这样处理。
    """
    session_generator = get_mysql_session()
    session = next(session_generator)
    try:
        update_popular_wishlist(session)
    finally:
        session.close()


def start_scheduler():
    # 每周一凌晨3点触发
    trigger = CronTrigger(day_of_week="mon", hour=3, minute=0)
    scheduler.add_job(
        update_steam_cache, trigger, id="steam_app_cache_update", replace_existing=True
    )

    # 每周一凌晨3:05触发更新 popular_wishlist 数据任务
    wishlist_trigger = CronTrigger(day_of_week="tue", hour=3, minute=10)
    scheduler.add_job(
        update_popular_wishlist_wrapper,
        wishlist_trigger,
        id="popular_wishlist_update",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("定时任务已启动")


def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("定时任务已关闭")
