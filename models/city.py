#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"

    state_id = Column(
        'state_id', Integer, ForeignKey('states.id'), nullable=False)
    name = Column('name', String(128), nullable=False)
