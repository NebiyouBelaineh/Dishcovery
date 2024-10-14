#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from os import environ
from dishcovery.models.base_model import BaseModel, Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

classes = {}
load_dotenv()


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __engine_without_db = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        DISHCOVERY_MYSQL_USER = environ.get('DISHCOVERY_MYSQL_USER')
        DISHCOVERY_MYSQL_PWD = environ.get('DISHCOVERY_MYSQL_PWD')
        DISHCOVERY_MYSQL_HOST = environ.get('DISHCOVERY_MYSQL_HOST',
                                            'dishcovery-mysql')
        DISHCOVERY_MYSQL_DB = environ.get('DISHCOVERY_MYSQL_DB')
        DISHCOVERY_ENV = environ.get('DISHCOVERY_ENV')
        # Create engine without database
        self.__engine_without_db = create_engine(
                                                'mysql+mysqldb://{}:{}@{}'
                                                .format(DISHCOVERY_MYSQL_USER,
                                                        DISHCOVERY_MYSQL_PWD,
                                                        DISHCOVERY_MYSQL_HOST))
        # Create the database if it does not exist
        try:
            with self.__engine_without_db.connect() as connection:
                connection.execute(text(
                    f"CREATE DATABASE IF NOT EXISTS {DISHCOVERY_MYSQL_DB}"))
                connection.execute(text(
                    f"USE {DISHCOVERY_MYSQL_DB}"))
                connection.execute(text(
                    f"""CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(36) PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\
                    ON UPDATE CURRENT_TIMESTAMP,
                    email VARCHAR(128) NOT NULL UNIQUE,
                    password VARCHAR(128) NOT NULL,
                    firstname VARCHAR(60),
                    lastname VARCHAR(60)
                    )"""))
                connection.execute(text(
                    f"""CREATE TABLE IF NOT EXISTS bookmarks (
                    id VARCHAR(36) PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\
                    ON UPDATE CURRENT_TIMESTAMP,
                    label TEXT NULL,
                    source VARCHAR(60) NULL,
                    image_link TEXT NULL,
                    ingredients TEXT NULL,
                    total_time FLOAT NULL DEFAULT 0,
                    calories FLOAT NULL DEFAULT 0.0,
                    link TEXT NULL,
                    tags TEXT NULL,
                    user_id VARCHAR(60) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE\
                    CASCADE
                    )"""))
        except Exception as e:
            print(f"DB Connection not successful: {e}")

        # Connect to the database with the connection url including db name
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(DISHCOVERY_MYSQL_USER,
                                             DISHCOVERY_MYSQL_PWD,
                                             DISHCOVERY_MYSQL_HOST,
                                             DISHCOVERY_MYSQL_DB))

        if DISHCOVERY_ENV == "test":
            BaseModel.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def getSession(self):
        return self.__session

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
