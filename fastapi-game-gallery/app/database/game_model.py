from sqlalchemy import Column, Integer, String, Text, Date, Enum, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# class Game(Base):
#     __tablename__ = "game"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), index=True, nullable=False)
#     release_date = Column(String(50), index=True, nullable=True)
#     platforms = Column(Text)
#     genres = Column(Text)
#     image_url = Column(String(255))
#     anticipation_rating = Column(Integer)
#     description = Column(Text)

#     def __repr__(self):
#         return f"<Game(id={self.id}, title={self.title}, release_date={self.release_date})>"


class GameRelease(Base):
    __tablename__ = "game_release"

    id = Column(Integer, primary_key=True, autoincrement=True)
    steam_id = Column(Integer, index=True, nullable=False)  # 允许多个版本
    name = Column(String(255), nullable=False)
    release_date = Column(Date, nullable=True)
    release_year = Column(Integer, nullable=True)
    release_quarter = Column(String(6), nullable=True)
    release_status = Column(
        Enum("To be announced", "Coming soon", name="release_status_enum"),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "(release_date IS NOT NULL AND release_year IS NULL AND release_quarter IS NULL) "
            "OR (release_quarter IS NOT NULL AND release_year IS NOT NULL AND release_date IS NULL) "
            "OR (release_year IS NOT NULL AND release_date IS NULL)",
            name="release_date_constraints",
        ),
    )

    def __repr__(self):
        return (
            f"<Game(name={self.name}, release_date={self.release_date}, "
            f"release_year={self.release_year}, release_quarter={self.release_quarter}, "
            f"release_status={self.release_status})>"
        )
