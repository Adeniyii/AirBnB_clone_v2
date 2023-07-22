#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    name = Column('name', String(128), nullable=False)

    # cities = relationship('City', back_populates='state',
    #                       cascade="all, delete, delete orphan")
