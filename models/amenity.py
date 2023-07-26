#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """The amenity class, contains name field and places relationship.
    """
    __tablename__ = "amenities"
    name = Column('name', String(128), nullable=False)
