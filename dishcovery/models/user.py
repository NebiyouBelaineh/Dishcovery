"""User class module"""

from models.base_model import BaseModel
from sqlalchemy import Column, String
from hashlib import md5

class User(BaseModel):
    """User class containing user information"""
    __tablename__ = "users"

    email = Column(String(128), unique=True, nullable=False)        
    password = Column(String(128), nullable=False) # Should be converted to md5
    firstname = Column(String(60), nullable=True)
    lastname = Column(String(60), nullable=True)

    def __init__(self):
        super().__init__()

    def __setattr__(self, name, value):
        """Sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)