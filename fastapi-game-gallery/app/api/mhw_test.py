import requests
import json

# 目标游戏的 Steam App ID
APP_ID = "2246340"

# Steam Store API 查询 URL
URL = f"https://store.steampowered.com/api/appdetails?appids={APP_ID}&cc=cn&l=schinese"

def get_steam_game_info(app_id):
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        if data[str(app_id)]["success"]:
            game_data = data[str(app_id)]["data"]
            print(game_data)
            return {
                "游戏名称": game_data.get("name", "N/A"),
                "游戏类型": ", ".join([genre["description"] for genre in game_data.get("genres", [])]),
                "发行商": ", ".join(game_data.get("publishers", [])),
                "开发商": ", ".join(game_data.get("developers", [])),
                "简要描述": game_data.get("short_description", "N/A"),
                "价格": game_data.get("price_overview", {}).get("final_formatted", "未知"),
                "封面图片": game_data.get("header_image", ""),
                "商店链接": f"https://store.steampowered.com/app/{app_id}/"
            }
    return None

# 获取游戏信息
game_info = get_steam_game_info(APP_ID)

if game_info:
    print(json.dumps(game_info, indent=4, ensure_ascii=False))
else:
    print("未能获取游戏信息")
