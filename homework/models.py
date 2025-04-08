from database import Base
from sqlalchemy import Column, Integer, String


class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    views_count = Column(Integer, default=0)
    cook_time = Column(Integer, nullable=False)
    ingredients = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)
