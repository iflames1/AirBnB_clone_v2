#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session

all_classes = {'State': State, 'City': City,
               'User': User, 'Place': Place,
               'Review': Review, 'Amenity': Amenity}


class DBStorage:
    """Database storage engine."""
    __engine = None
    __session = None

    def __init__(self):
        """"Instantiates a new DBStorage object."""
        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")

        HBNB_USER_DETAILS = f"{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}"
        URL_DETAILS = f"{HBNB_USER_DETAILS}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}"
        URL = f"mysql+mysqldb://{URL_DETAILS}"

        self.__engine = create_engine(
            URL, pool_pre_ping=True)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session (self.__session) all objects
          depending on the class name (argument cls)
        """
        new_dict = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                new_dict[key] = obj
        else:
            for cls in all_classes.values():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Add the object to the current database session (self.__session)
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session (self.__session)
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and create the current database
          session (self.__session)
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
