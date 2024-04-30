"""Bookmark class module"""
from dishcovery.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship


class Bookmark(BaseModel):
    """Bookmark class"""
    __tablename__ = "bookmarks"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    label = Column(String(60), nullable=True)
    image_link = Column(String(60), nullable=True)
    ingredients = Column(Text, nullable=True)  # imported from a list
    preparation_time = Column(Integer, nullable=True, default=0)
    calorie_intake = Column(Float, nullable=True, default=0.0)
    link = Column(String(60), nullable=True)
    tags = Column(Text, nullable=True)
    cousine_type = Column(Text, nullable=True)

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    # recipe_id = Column(String(60), ForeignKey('recipes.id'), nullable=False)
