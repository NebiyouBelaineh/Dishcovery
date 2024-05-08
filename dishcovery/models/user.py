"""User class module"""


from dishcovery import login_manager
from dishcovery.models.base_model import BaseModel
from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


"""
disable to create tables;
"""


@login_manager.user_loader
def load_user(user_id):
    from dishcovery.models import db_storage
    return db_storage.getSession().query(User).get(user_id)


class User(BaseModel, UserMixin):
    """User class containing user information"""
    __tablename__ = "users"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    firstname = Column(String(60), nullable=True)
    lastname = Column(String(60), nullable=True)
    bookmarks = relationship('Bookmark',
                             backref='users',
                             cascade="all, delete, delete-orphan")

    def __setattr__(self, name, value):
        """Sets a password with md5 encryption"""
        from dishcovery import bcrypt
        if name == "password":
            # value = md5(value.encode()).hexdigest()
            value = bcrypt.generate_password_hash(value).decode('utf-8')
        super().__setattr__(name, value)

    def check_password(self, attempted_password):
        from dishcovery import bcrypt
        return bcrypt.check_password_hash(self.password, attempted_password)

    def full_name(self):
        return f'{self.firstname.capitalize()} {self.lastname.capitalize()}'
