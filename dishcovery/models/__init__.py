#!/usr/bin/python3
"""
initialize the models package
"""

from dishcovery.models.engine.db_storage import DBStorage
from os import getenv


storage = DBStorage()
storage.reload()
