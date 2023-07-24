#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"

    name = Column('name', String(128), nullable=False)
    state_id = Column(
        'state_id', String(60), ForeignKey('states.id'), nullable=False)
    places = relationship(
        'Place', backref="cities", cascade="all, delete, delete-orphan")
