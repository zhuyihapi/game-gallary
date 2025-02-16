import requests

# 获取 Steam 游戏列表
API_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

def get_steam_app_id(game_name):
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        for app in data["applist"]["apps"]:
            if app["name"].lower() == game_name.lower():
                return app["appid"]
    return None

# 查询 Monster Hunter Wilds 的 App ID
game_name = "Monster Hunter Wilds"
app_id = get_steam_app_id(game_name)

if app_id:
    print(f"Steam App ID for {game_name}: {app_id}")
else:
    print(f"Game '{game_name}' not found in Steam App List.")
