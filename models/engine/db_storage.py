#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""


class DBStorage:
    """This class manages the storage of HBNB models in a mysql database"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        from sqlalchemy import create_engine
        from sqlalchemy.schema import MetaData
        import os

        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        env = os.getenv('HBNB_ENV')

        engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, env),
            pool_pre_ping=True)

        self.__engine = engine
        self.__metadata_obj = MetaData()

        if (os.environ.get('HBNB_TYPE_STORAGE') == 'test'):
            MetaData.drop_all(bind=self.__engine, checkfirst=True)

    def all(self, cls=None):
        """Returns a dictionary of model instances from the database"""
        result = []
        if cls is None:
            tables = self.__metadata_obj.tables
            for k, v in tables.items():
                result.append(self.__session.query(v).all())
                # result.append(v.select().columns)
        else:
            result.append(self.__session.query(cls).all())

        return result

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
        from sqlalchemy.orm import sessionmaker, scoped_session

        session_factory = sessionmaker(self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
        self.__metadata_obj.create_all(bind=self.__engine)
