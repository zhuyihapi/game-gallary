from re import A
import requests
import requests
from typing import Optional
from loguru import logger
from app.config import twitch_settings


TWITCH_ACCESS_TOKEN = twitch_settings.TWITCH_ACCESS_TOKEN
TWITCH_CLIENT_ID = twitch_settings.TWITCH_CLIENT_ID
TWITCH_CLIENT_SECRET = twitch_settings.TWITCH_CLIENT_SECRET


# 检查 Access Token 是否有效
def is_access_token_valid(access_token: str) -> bool:
    url = "https://id.twitch.tv/oauth2/validate"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logger.debug("TWITCH_ACCESS_TOKEN valid")
        return True
    else:
        logger.debug("TWITCH_ACCESS_TOKEN invalid, need to get a new one")
        return False


# 获取新的 Access Token
def get_new_access_token(client_id: str, client_secret: str) -> Optional[str]:
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
        print(f"get a new Access Token: {new_token}")
    else:
        print(f"fail to get a new token, find error message: {response_data}")

    return new_token


# 检查 Token 并获取有效 Token
def check_or_get_access_token() -> str:
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
