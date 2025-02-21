from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

from app.logger import logger


def parse_popular_wishlist():
    """
    Parses the 'popularwishlist.html' file and extracts game information.

    Returns:
        pd.DataFrame: A DataFrame containing game ID, name, and release date.
    """
    try:
        # Determine the file path
        file_path = Path(__file__).resolve().parent.parent / "resource" / "popularwishlist.html"
        logger.debug(f"Attempting to get popular-wishlist HTML file path: {file_path}")

        # Read the file
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return pd.DataFrame(columns=["ID", "Game", "Release Date"])  # Return empty DataFrame
        
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
                game_name = game.find("span", class_="title").text.strip() if game.find("span", class_="title") else "Unknown"
                release_date = game.find("div", class_="search_released").text.strip() if game.find("div", class_="search_released") else "TBD"

                if game_id and game_name:
                    games.append((game_id, game_name.replace(" ", "_"), release_date))  # Replace spaces with underscores
                
            except Exception as e:
                logger.warning(f"Failed to parse game element: {game}. Error: {e}")

        # Convert to DataFrame
        df = pd.DataFrame(games, columns=["ID", "Game", "Release Date"])
        logger.info(f"Successfully parsed {len(df)} games from the wishlist.")

        return df

    except Exception as e:
        logger.exception(f"An unexpected error occurred while parsing the wishlist: {e}")
        return pd.DataFrame(columns=["ID", "Game", "Release Date"])  # Return empty DataFrame

# Example usage
if __name__ == "__main__":
    df = parse_popular_wishlist()
    print(df)
