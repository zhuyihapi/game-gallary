from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import aiohttp

from app.api.steam_store_match import fetch_steam_app_list
from app.logger import logger

scheduler = AsyncIOScheduler()


def update_steam_cache():
    # logger.info(f"[{datetime.now()}] 正在更新 Steam App 缓存...")
    data = fetch_steam_app_list()
    if data:
        logger.info(f"[{datetime.now()}] Steam App 缓存更新完成（共 {len(data['applist']['apps'])} 个应用）")
    else:
        logger.info(f"[{datetime.now()}] Steam App 缓存更新失败")

def start_scheduler():
    # 每天凌晨3点触发
    trigger = CronTrigger(hour=3, minute=0)
    scheduler.add_job(update_steam_cache, trigger, id="steam_app_cache_update", replace_existing=True)
    scheduler.start()
    logger.info("定时任务已启动")

def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("定时任务已关闭")
