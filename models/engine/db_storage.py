#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """It represents DBStorage engine"""

    storage = getenv('HBNB_TYPE_STORAGE')
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes DBStorage """
        db_user = getenv("HBNB_MYSQL_USER")
        db_pwd = getenv("HBNB_MYSQL_PWD")
        db_host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")

        db_url = f"mysql+mysqldb://{db_user}:{db_pwd}@{db_host}/{db_name}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all objects of the given class
        If cls is None, query all types of objects and
        returns dictionary of the queried classes
        """

        if cls in None:
            objects = []
            classes = [State, City, User, Place, Review, Amenity]
            for class_type in classes:
                objects.extend(self.__session.query(class_type).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)

    def new(self, obj):
        """adds new object to the database"""
        self.__session.add(obj)

    def save(self):
        """saves the added object"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes object from the database"""
        self.__session.delete(obj)

    def reload(self):
        """reloads and waits for a new session"""

        Base.metadata.create_all(self.__engine)
        new_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(new_session)
        self.__session = Session()

    def close(self):
        """call remove() or close() method on the private session attribute"""
        self.__session.close()
