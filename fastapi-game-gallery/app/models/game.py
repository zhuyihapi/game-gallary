from sqlalchemy import Column, Integer, String, Text
from app.database.mysql import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    release_date = Column(String, index=True)
    platforms = Column(Text)
    genres = Column(Text)
    image_url = Column(String)
    anticipation_rating = Column(Integer)
    description = Column(Text)