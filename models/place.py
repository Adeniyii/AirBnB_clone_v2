#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base, place_amenity
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(
        'city_id', String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(
        'user_id', String(60), ForeignKey('users.id'), nullable=False)
    name = Column("name", String(128), nullable=False)
    description = Column("description", String(1024), nullable=False)
    number_rooms = Column("number_rooms", Integer(), nullable=False, default=0)
    number_bathrooms = Column(
        "number_bathrooms", Integer(), nullable=False, default=0)
    max_guest = Column("max_guest", Integer(), nullable=False, default=0)
    price_by_night = Column(
        "price_by_night", Integer(), nullable=False, default=0)
    latitude = Column("latitude", Float(), nullable=False, default=0)
    longitude = Column("longitude", Float(), nullable=False, default=0)
    reviews = relationship(
        "Review", backref="place", cascade="all, delete, delete-orphan")
    amenity_ids = []
    place_amenity = place_amenity
    # many to many Place<->Amenity
    amenities = relationship(
        'Amenity', secondary=place_amenity, back_populates='places', viewonly=False)  # noqa

    @property
    def reviews(self):
        """Return a list of reviews with place_id equal to the current Place.id
        """
        from models import storage

        all_reviews = storage.all("review")
        review_list = []

        for _, v in all_reviews:
            if v.get('place_id') == Place.id:
                review_list.append(v)

        return review_list
