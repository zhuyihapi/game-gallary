from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import requests

from app.logger import logger
from app.config import ROOT_DIR

CACHE_DIR = ROOT_DIR / "app" / ".cache"


def temp_save_to_mysql(df, session):
    """
    将 DataFrame 中的数据保存到 MySQL 数据库中，使用传入的 session 进行操作。

    参数:
        df (pd.DataFrame): 要保存的数据
        session: SQLAlchemy Session 对象，由依赖注入或其它方式提供
    """
    try:
        # 通过 session.get_bind() 获取绑定的 engine
        engine = session.get_bind()
        df.to_sql("popular_wishlist", con=engine, if_exists="append", index=False)
        logger.info("数据成功写入 MySQL 数据库。")
    except Exception as e:
        logger.exception(f"数据写入 MySQL 失败: {e}")


def get_popular_wishlist(start, count) -> str:
    """
    获取指定起始位置和条数的Steam搜索结果，并将页面保存到本地。
    注意：这里保存的文件名为 steam_page_{start}_{start+count}.html，
    如果希望parse时读取固定名称的文件，请自行调整保存路径或文件名。
    """
    url = f"https://store.steampowered.com/search/?filter=popularwishlist&start={start}&count={count}"
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"请求失败，状态码：{response.status_code}")
        return None

    # 保存页面到当前目录，你也可以指定其它目录（例如resource目录）
    filename = f"steam_page_{start}_{start+count}.html"
    with open(CACHE_DIR / filename, "w", encoding="utf-8") as f:
        f.write(response.text)
    logger.info(f"popular wishlist saved to {filename}")

    return filename


def parse_popular_wishlist(file_path):
    """
    Parses the 'popularwishlist.html' file and extracts game information.

    Returns:
        pd.DataFrame: A DataFrame containing game ID, name, and release date.
    """
    try:
        # Determine the file path
        if not file_path:
            file_path = CACHE_DIR / "popularwishlist.html"
            logger.debug(
                f"Attempting to get popular-wishlist HTML file path: {file_path}"
            )

        # Read the file
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return pd.DataFrame(
                columns=["ID", "Game", "Release Date"]
            )  # Return empty DataFrame

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(content, "html.parser")

        # Find game elements
        game_elements = soup.find_all("a", class_="search_result_row")

        # Extract game details
        games = []
        for game in game_elements:
            try:
                game_id = game.get("data-ds-appid", "").strip()  # Steam App ID
                game_name = (
                    game.find("span", class_="title").text.strip()
                    if game.find("span", class_="title")
                    else "Unknown"
                )
                release_date = (
                    game.find("div", class_="search_released").text.strip()
                    if game.find("div", class_="search_released")
                    else "TBD"
                )

                if game_id and game_name:
                    games.append(
                        (game_id, game_name.replace(" ", "_"), release_date)
                    )  # Replace spaces with underscores

            except Exception as e:
                logger.warning(f"Failed to parse game element: {game}. Error: {e}")

        # Convert to DataFrame
        df = pd.DataFrame(games, columns=["ID", "Game", "Release Date"])
        logger.info(f"Successfully parsed {len(df)} games from the wishlist.")

        return df

    except Exception as e:
        logger.exception(
            f"An unexpected error occurred while parsing the wishlist: {e}"
        )
        return pd.DataFrame(
            columns=["ID", "Game", "Release Date"]
        )  # Return empty DataFrame


if __name__ == "__main__":
    df = parse_popular_wishlist()
    print(df)
