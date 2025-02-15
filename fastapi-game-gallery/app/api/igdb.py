import requests
import datetime
import time

# Twitch API 认证信息
CLIENT_ID = "lx58mgtbnhy6j9pnmyi00o3mxwi9vd"
CLIENT_SECRET = "1in6s03qwzfv52lwh15q6wmivdqf90"
ACCESS_TOKEN = "bloz1rxb1ea1bpqg03ry5qp3qz0rbt"

# 获取 Access Token
def check_or_get_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    response_data = response.json()
    return response_data.get("access_token")

# ✅ 获取本月起始和结束时间（Unix 时间戳）
def get_current_month_timestamp():
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)  # 本月1号
    next_month = today.month % 12 + 1
    next_year = today.year + (1 if today.month == 12 else 0)
    end_date = datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)  # 本月最后一天

    start_timestamp = int(time.mktime(start_date.timetuple()))  # 转换为Unix时间戳
    end_timestamp = int(time.mktime(end_date.timetuple()))
    return start_timestamp, end_timestamp

# ✅ 查询本月发售的游戏
def get_games_released_this_month(access_token):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    start_timestamp, end_timestamp = get_current_month_timestamp()

    # 📌 查询 IGDB `release_dates` API，获取本月发布的游戏
    query = f'''
        fields game, human, platform, date;
        where date >= {start_timestamp} & date <= {end_timestamp};
        sort date asc;
        limit 50;
    '''
    response = requests.post("https://api.igdb.com/v4/release_dates/", headers=headers, data=query)
    release_dates_data = response.json()

    if not release_dates_data:
        print("❌ 没有找到本月发售的游戏")
        return []

    # 📌 提取游戏 ID
    game_ids = list(set([game["game"] for game in release_dates_data]))
    return game_ids, release_dates_data

# ✅ 获取游戏详细信息
def get_game_details(access_token, game_ids):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    # 📌 查询 IGDB `games` API，获取详细信息
    game_id_str = ",".join(map(str, game_ids))
    query = f'''
        fields id, name, summary, genres, platforms, cover.url;
        where id = ({game_id_str});
        limit 50;
    '''
    response = requests.post("https://api.igdb.com/v4/games/", headers=headers, data=query)
    return response.json()

# ✅ 获取平台名称（可选）
def get_platform_names(access_token, platform_ids):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    query = f'''
        fields id, name;
        where id = ({",".join(map(str, platform_ids))});
    '''
    response = requests.post("https://api.igdb.com/v4/platforms/", headers=headers, data=query)
    platform_data = response.json()
    return {p["id"]: p["name"] for p in platform_data}

# ✅ 运行主流程
def main():
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 Access Token")
        return

    # 获取本月发售的游戏 ID
    game_ids, release_dates_data = get_games_released_this_month(access_token)
    if not game_ids:
        return

    # 获取游戏详细信息
    game_details = get_game_details(access_token, game_ids)

    # 获取所有涉及的平台 ID
    all_platform_ids = set()
    for game in release_dates_data:
        all_platform_ids.update(game["platform"])
    platform_names = get_platform_names(access_token, all_platform_ids)

    # 🔥 显示结果
    print("\n🎮 本月发布的游戏列表：\n")
    for game in game_details:
        game_id = game["id"]
        game_name = game.get("name", "未知游戏")
        game_summary = game.get("summary", "无简介")
        cover_url = game.get("cover", {}).get("url", "")
        platforms = [platform_names.get(pid, f"平台ID {pid}") for pid in game.get("platforms", [])]
        
        release_info = [rd for rd in release_dates_data if rd["game"] == game_id]
        release_dates = ", ".join([rd["human"] for rd in release_info])

        print(f"🎮 游戏名: {game_name}")
        print(f"📅 发行日期: {release_dates}")
        print(f"🕹️  平台: {', '.join(platforms) if platforms else '未知'}")
        print(f"📖 简介: {game_summary}")
        if cover_url:
            print(f"🖼️ 封面: https:{cover_url}")
        print("-" * 50)

# ✅ 运行脚本
if __name__ == "__main__":
    main()
