#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column('name', String(128), nullable=False)

    cities = relationship(
        'City', backref="state", cascade="all, delete, delete-orphan")

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """Return a list of cities with state_id equal to the current State.id"""  # noqa
            from models import storage
            from models.city import City

            all_cities = storage.all(City)
            cities_list = []

            for _, v in all_cities.items():
                if v.state_id == self.id:
                    cities_list.append(v)

            return cities_list
