from pathlib import Path
import requests
import json
import os
import time

from app.config import ROOT_DIR

current_file = Path(__file__)
API_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
CACHE_DIR = ROOT_DIR / "app" / ".cache"
CACHE_FILE = os.path.join(CACHE_DIR, "steam_apps_cache.json")
CACHE_EXPIRE_TIME = 86400  # 1天（单位：秒）


def fetch_steam_app_list():
    """从Steam API获取游戏列表，并缓存到本地文件"""
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()

        # 确保缓存目录存在
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {"timestamp": time.time(), "data": data},
                f,
                ensure_ascii=False,
                indent=4,
            )
        return data
    return None


def load_cached_app_list():
    """加载本地缓存的游戏列表，如果过期则重新获取"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
            if time.time() - cache["timestamp"] < CACHE_EXPIRE_TIME:
                return cache["data"]

    return fetch_steam_app_list()  # 缓存不存在或过期，重新获取


def get_steam_app_id(game_name):
    """查询游戏ID"""
    data = load_cached_app_list()
    if data:
        for app in data["applist"]["apps"]:
            if game_name.strip().lower() in app["name"].strip().lower():
                return app["appid"]
    return None


# 查询游戏
game_name = "Monster Hunter Wilds"
app_id = get_steam_app_id(game_name)

if __name__ == "__main__":
    if app_id:
        print(f"Steam App ID for {game_name}: {app_id}")
    else:
        print(f"Game '{game_name}' not found in Steam App List.")
