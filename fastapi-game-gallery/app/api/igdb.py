import requests
import datetime
import time

from app.api.igdb_token import (
    TWITCH_ACCESS_TOKEN,
    TWITCH_CLIENT_ID,
    check_or_get_access_token,
)


# 获取本月起始和结束时间（Unix 时间戳）
def get_current_month_timestamp() -> tuple[int, int]:
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)  # 本月1号
    next_month = today.month % 12 + 1
    next_year = today.year + (1 if today.month == 12 else 0)
    end_date = datetime.date(next_year, next_month, 1) - datetime.timedelta(
        days=1
    )  # 本月最后一天

    start_timestamp = int(time.mktime(start_date.timetuple()))  # 转换为Unix时间戳
    end_timestamp = int(time.mktime(end_date.timetuple()))
    return start_timestamp, end_timestamp


# 获取本周起始和结束时间（Unix 时间戳）
def get_current_week_timestamp() -> tuple[int, int]:
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=today.weekday())  # 本周一
    end_date = start_date + datetime.timedelta(days=6)  # 本周日

    start_timestamp = int(time.mktime(start_date.timetuple()))  # 转换为Unix时间戳
    end_timestamp = int(time.mktime(end_date.timetuple()))
    return start_timestamp, end_timestamp


# 获取某天起始和结束时间（Unix 时间戳）
def get_day_timestamp(date: datetime.date) -> tuple[int, int]:
    start_timestamp = int(time.mktime(date.timetuple()))  # 当天开始时间的Unix时间戳
    end_timestamp = (
        start_timestamp + 86400 - 1
    )  # 当天结束时间的Unix时间戳（86400秒为一天）
    return start_timestamp, end_timestamp


# 查询一段时间发售的游戏
def get_games_released_this_month() -> tuple[list[int], list[dict]]:
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}",
        "Accept": "application/json",
    }
    # start_timestamp, end_timestamp = get_current_month_timestamp()
    start_timestamp, end_timestamp = get_day_timestamp(datetime.date(2025, 2, 28))

    # 查询 IGDB `release_dates` API，获取发布的游戏
    query = f"""
        fields game, human, platform, date;
        where date >= {start_timestamp} & date <= {end_timestamp};
        sort date asc;
        limit 50;
    """
    response = requests.post(
        "https://api.igdb.com/v4/release_dates/", headers=headers, data=query
    )
    release_dates_data = response.json()

    if not release_dates_data:
        print("没有找到本月发售的游戏")
        return [], []

    # 提取游戏 ID
    game_ids = list(set([game["game"] for game in release_dates_data]))
    return game_ids, release_dates_data


# 获取游戏详细信息
def get_game_details(game_ids: list[int]) -> list[dict]:
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}",
        "Accept": "application/json",
    }

    # 查询 IGDB `games` API，获取详细信息
    game_id_str = ",".join(map(str, game_ids))
    query = f"""
        fields id, name, summary, genres, platforms, cover.url;
        where id = ({game_id_str});
        limit 50;
    """
    response = requests.post(
        "https://api.igdb.com/v4/games/", headers=headers, data=query
    )
    time.sleep(0.25)  # 确保每秒请求不超过4个
    return response.json()


# 获取平台名称（可选）
def get_platform_names(platform_ids: set[int]) -> dict[int, str]:
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}",
        "Accept": "application/json",
    }
    query = f"""
        fields id, name;
        where id = ({",".join(map(str, platform_ids))});
    """
    response = requests.post(
        "https://api.igdb.com/v4/platforms/", headers=headers, data=query
    )
    time.sleep(0.25)  # 确保每秒请求不超过4个
    platform_data = response.json()
    return {p["id"]: p["name"] for p in platform_data}


# 运行测试主流程
def test() -> None:
    check_or_get_access_token()

    # 获取本月发售的游戏 ID
    game_ids, release_dates_data = get_games_released_this_month()
    if not game_ids:
        return

    # 获取游戏详细信息
    game_details = get_game_details(game_ids)

    # 获取所有涉及的平台 ID
    all_platform_ids = set()
    for game in release_dates_data:
        platforms = game.get("platform", [])
        if isinstance(platforms, list):
            all_platform_ids.update(platforms)
        else:
            all_platform_ids.add(platforms)
    platform_names = get_platform_names(all_platform_ids)

    # 显示结果
    print("\n🎮 本月发布的游戏列表：\n")
    for game in game_details:
        game_id = game["id"]
        game_name = game.get("name", "未知游戏")
        game_summary = game.get("summary", "无简介")
        cover_url = game.get("cover", {}).get("url", "")
        platforms = [
            platform_names.get(pid, f"平台ID {pid}")
            for pid in game.get("platforms", [])
        ]

        release_info = [rd for rd in release_dates_data if rd["game"] == game_id]
        release_dates = ", ".join([rd["human"] for rd in release_info])

        print(f"🎮 游戏名: {game_name}")
        print(f"发行日期: {release_dates}")
        print(f"平台: {', '.join(platforms) if platforms else '未知'}")
        print(f"简介: {game_summary}")
        if cover_url:
            print(f"封面: https:{cover_url}")
        print("-" * 50)


# 运行脚本
if __name__ == "__main__":
    test()
