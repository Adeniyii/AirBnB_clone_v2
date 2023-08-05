#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""


class DBStorage:
    """This class manages the storage of HBNB models in a mysql database"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        from sqlalchemy import create_engine
        from models.base_model import Base
        import os

        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')

        engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db),
            pool_pre_ping=True)

        self.__engine = engine
        self.__metadata_obj = Base.metadata

        if (os.getenv('HBNB_TYPE_STORAGE') == 'test'):
            self.__metadata_obj.drop_all(bind=self.__engine, checkfirst=True)

    def all(self, cls=None):
        """Returns a dictionary of model instances from the database"""
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity

        classes = [User, Place, State, City, Amenity, Review]
        result_map = {}
        objects = []

        if cls:
            objects = self.__session.query(cls).all()
            for object in objects:
                dictified = object.to_dict()
                result_map.update(
                    {dictified['__class__'] + '.' + object.id: object})
        else:
            for cls in classes:
                objects.append(self.__session.query(cls).all())

            for object_list in objects:
                for object in object_list:
                    dictified = object.to_dict()
                    result_map.update(
                        {dictified['__class__'] + '.' + object.id: object})

        return result_map

    def new(self, obj=None):
        """Add a new object to the current session"""
        if obj is None:
            return None
        self.__session.add(obj)

    def save(self):
        """Commit all session changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the passed object from the database"""
        if obj is None:
            return None
        self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        from models.city import City
        from models.state import State
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        from sqlalchemy.orm import sessionmaker, scoped_session

        self.__metadata_obj.create_all(bind=self.__engine)

        session_factory = sessionmaker(self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """close the current session"""
        self.__session.remove()
