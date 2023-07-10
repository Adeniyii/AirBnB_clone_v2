#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""


class DBStorage:
    """This class manages the storage of HBNB models in a mysql database"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.schema import MetaData
        import os

        Session = sessionmaker(bind=self.__engine)

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_ENV')), pool_pre_ping=True)

        self.__session = Session()
        self.__metadata_obj = MetaData()

        if (os.environ.get('HBNB_TYPE_STORAGE') == 'test'):
            MetaData.drop_all(bind=self.__engine, checkfirst=True)

    def all(self, cls=None):
        """Returns a dictionary of model instances from the database"""
        if cls is None:
            tables = self.__metadata_obj.tables
            for k, v in tables.items():
                v.select().order_by(None)
