#!/usr/bin/python3
"""
initialize the models package
"""

from dishcovery.models.engine.db_storage import DBStorage

# Initialize DBStorage object and create tables
db_storage = DBStorage()

# Import model classes after initializing tables
from dishcovery.models.user import User
from dishcovery.models.recipe import Recipe
from dishcovery.models.bookmark import Bookmark
