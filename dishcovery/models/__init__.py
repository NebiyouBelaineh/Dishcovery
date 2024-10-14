#!/usr/bin/python3
"""
initialize the models package
"""

from dishcovery.models.engine.db_storage import DBStorage

# Initialize DBStorage object and create tables
db_storage = DBStorage()
db_storage.reload()
