from bs4 import BeautifulSoup
from pathlib import Path
from loguru import logger
import pandas as pd
import requests
import aiohttp
import aiofiles


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


async def get_popular_wishlist(start: int, count: int) -> str | None:
    """
    异步获取指定起始位置和条数的 Steam 搜索结果，
    并将页面保存到本地。
    保存文件名：steam_page_{start}_{start+count}.html
    """
    url = (
        "https://store.steampowered.com/search/"
        f"?filter=popularwishlist&start={start}&count={count}"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                logger.error(f"请求失败，状态码：{resp.status}")
                return None
            text = await resp.text()

    filename = f"steam_page_{start}_{start+count}.html"
    target = CACHE_DIR / filename
    target.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(target, mode="w", encoding="utf-8") as f:
        await f.write(text)

    logger.info(f"popular wishlist saved to {filename}")
    
    return filename


def parse_popular_wishlist(
    cache_name: str = None, test_cache_path: str = None
) -> pd.DataFrame:
    """
    Parses the 'popularwishlist.html' or 'steam_page_*_*.html' file and extracts game information.

    Returns:
        pd.DataFrame: A DataFrame containing game ID, name, and release date.
    """
    try:
        # Determine the file path
        if not cache_name and not test_cache_path:
            logger.debug(f"cache_name is empty!")
            raise ValueError("cache_name must be provided")

        # Read the file
        if test_cache_path:
            cache_path= Path(test_cache_path)
        else:
            cache_path = CACHE_DIR / Path(cache_name)
        if not cache_path.exists():
            logger.error(f"File not found: {cache_path}")
            return pd.DataFrame(
                columns=["ID", "Game", "Release Date"]
            )  # Return empty DataFrame

        with open(cache_path, "r", encoding="utf-8") as file:
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
    df = parse_popular_wishlist(test_cache_path="/home/ubuntu/projects/game-gallary/fastapi-game-gallery/app/.cache/steam_page_0_50.html")
    print(df)
