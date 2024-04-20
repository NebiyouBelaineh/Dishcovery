"""Bookmark class module"""
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey


class Bookmark(BaseModel):
    """Bookmark class"""
    __tablename__ = "bookmarks"

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    recipe_id = Column(String(60), ForeignKey('recipes.id'), nullable=False)

    def __init__(self):
        super().__init__()
