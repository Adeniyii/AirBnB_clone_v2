#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = "reviews"

    text = Column("text", String(1024), nullable=False)
    place_id = Column(
        "place_id", String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(
        "user_id", String(60), ForeignKey("users.id"), nullable=False)
