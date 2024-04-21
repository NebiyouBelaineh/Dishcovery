"""Bookmark class module"""
from dishcovery.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Bookmark(BaseModel):
    """Bookmark class"""
    __tablename__ = "bookmarks"

    def __init__(self):
        super().__init__()

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    recipe_id = Column(String(60), ForeignKey('recipes.id'), nullable=False)

    # user = relationship("User", back_populates="bookmarks")
    recipe = relationship("Recipe", back_populates="bookmark", uselist=False)
