"""Bookmark class module"""
from dishcovery.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship


class Bookmark(BaseModel):
    """Bookmark class"""
    __tablename__ = "bookmarks"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    label = Column(Text, nullable=True)
    source = Column(String(60), nullable=True)
    image_link = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=True)  # imported from a list
    total_time = Column(Float, nullable=True, default=0)
    calories = Column(Float, nullable=True, default=0.0)
    link = Column(Text, nullable=True)  # fulldetails
    tags = Column(Text, nullable=True)

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    # recipe_id = Column(String(60), ForeignKey('recipes.id'), nullable=False)
