from typing import List
from loguru import logger

from app.schemas.game import Game


async def get_data_by_year_months(year_months: List[str]) -> List[Game]:
    """
    根据多个年月获取数据
    Args:
        year_months: 包含年月列表的请求参数
    Returns:
        List[Game]: 游戏数据列表
    """
    
    # 这里是一个示例实现，实际实现可能需要从数据库或其他数据源获取数据
    games = []
    
    for ym in year_months:
        # 模拟从数据库获取数据
        games.append(Game(id=len(games) + 1, title=f"Game {len(games) + 1}", release_date=ym))
    
    return games
