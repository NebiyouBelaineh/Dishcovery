"""Recipe class module"""
from dishcovery.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Float, Integer, Text
from sqlalchemy.orm import relationship


class Recipe(BaseModel):
    """Recipe class"""
    __tablename__ = "recipes"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # bookmark_id = Column(String(60), ForeignKey('bookmarks.id'),
    #                      nullable=False)
    label = Column(String(60), nullable=True)
    image_link = Column(String(60), nullable=True)
    ingredients = Column(Text, nullable=True)  # imported from a list
    preparation_time = Column(Integer, nullable=True, default=0)
    calorie_intake = Column(Float, nullable=True, default=0.0)
    link = Column(String(60), nullable=True)
    tags = Column(Text, nullable=True)
    cousine_type = Column(Text, nullable=True)

    # bookmark = relationship('Bookmark', back_populates='recipe',
    # uselist=False)
    # One-to-Many (reverse relationship)
    recipe_owner = relationship("User", backref='recipes')
