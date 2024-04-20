"""Recipe class module"""
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Float, Integer


class Recipe(BaseModel):
    """Recipe class"""
    __tablename__ = "recipes"

    bookmark_id = Column(String(60), ForeignKey('bookmarks.id'), nullable=False)
    label = Column(String(60), nullable=True)
    image_link = Column(String(60), nullable=True)
    ingredients = Column(String(60), nullable=True) # imported from a list
    preparation_time = Column(Integer(60), nullable=True, default=0)
    calorie_intake = Column(Float(60), nullable=True, default=0.0)
    link = Column(String(60), nullable=True)
    tags = Column(String(60), nullable=True)
    cousine_type = Column(String(60), nullable=True)
    cousine_type = Column(String(60), nullable=True)

    def __init__(self):
        super().__init__()
