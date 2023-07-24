#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, place_amenity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """The amenity class, contains name
    """
    __tablename__ = "amenities"
    name = Column('name', String(128), nullable=False)
    # many to many Place<->Amenity
    places = relationship(
        'Place', secondary=place_amenity, back_populates='amenities', viewonly=False)  # noqa
