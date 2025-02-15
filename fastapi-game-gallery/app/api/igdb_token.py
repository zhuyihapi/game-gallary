from re import A
import requests
import datetime
import time
import requests

from app.core.config import twitch_settings

TWITCH_ACCESS_TOKEN = twitch_settings.TWITCH_ACCESS_TOKEN
TWITCH_CLIENT_ID = twitch_settings.TWITCH_CLIENT_ID
TWITCH_CLIENT_SECRET = twitch_settings.TWITCH_CLIENT_SECRET


# 检查 Access Token 是否有效
def is_access_token_valid(access_token):
    url = "https://id.twitch.tv/oauth2/validate"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("-Access Token 有效")
        return True
    else:
        print("-Access Token 失效，需要重新获取")
        return False


# 获取新的 Access Token
def get_new_access_token(client_id, client_secret):
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params=params)
    response_data = response.json()

    new_token = response_data.get("access_token")
    if new_token:
        print(f"获取新的 Access Token: {new_token}")
    else:
        print(f"无法获取 Access Token, 错误信息: {response_data}")

    return new_token


# 检查 Token 并获取有效 Token
def check_or_get_access_token():
    global TWITCH_ACCESS_TOKEN
    if not is_access_token_valid(
        TWITCH_ACCESS_TOKEN
    ):  # 如果 Token 失效，则获取新 Token
        TWITCH_ACCESS_TOKEN = get_new_access_token()
    return TWITCH_ACCESS_TOKEN


# 运行测试
if __name__ == "__main__":
    token = check_or_get_access_token()
    print(f"-当前 Access Token: {token}")
