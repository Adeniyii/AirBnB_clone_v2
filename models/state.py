#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column('name', String(128), nullable=False)

    cities = relationship(
        'City', backref="state", cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """Return a list of cities with state_id equal to the current State.id
        """
        from models import storage

        all_cities = storage.all("city")
        cities_list = []

        for _, v in all_cities:
            if v.get('state_id') == State.id:
                cities_list.append(v)

        return cities_list
