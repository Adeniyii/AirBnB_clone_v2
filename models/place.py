#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
import os

place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),  # noqa
        Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)  # noqa
    )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(
        'city_id', String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(
        'user_id', String(60), ForeignKey('users.id'), nullable=False)
    name = Column("name", String(128), nullable=False)
    description = Column("description", String(1024))
    number_rooms = Column("number_rooms", Integer(), nullable=False, default=0)
    number_bathrooms = Column(
        "number_bathrooms", Integer(), nullable=False, default=0)
    max_guest = Column("max_guest", Integer(), nullable=False, default=0)
    price_by_night = Column(
        "price_by_night", Integer(), nullable=False, default=0)
    latitude = Column("latitude", Float())
    longitude = Column("longitude", Float())
    reviews = relationship(
        "Review", backref="place", cascade="all, delete, delete-orphan")
    amenity_ids = []
    # many to many Place<->Amenity
    amenities = relationship(
        'Amenity', secondary=place_amenity, backref="places", viewonly=False)  # noqa

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def reviews(self):
            """Return a list of reviews with place_id equal to the current Place.id"""  # noqa
            from models import storage
            from models.review import Review

            all_reviews = storage.all(Review)
            review_list = []

            for _, v in all_reviews:
                if v.get('place_id') == Place.id:
                    review_list.append(v)

            return review_list

        @property
        def amenities(self):
            """Return a list of reviews with place_id equal to the current Place.id  # noqa
            """
            from models import storage
            from models.amenity import Amenity

            all_amenities = storage.all(Amenity)
            amenity_list = []

            for _, v in all_amenities:
                if v.get('place_id') == Place.id:
                    amenity_list.append(v)

            return amenity_list
