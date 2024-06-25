#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage

place_amenity = Table('place_amenity', Base.metadata,
                      Column(
                          'place_id', String(60), ForeignKey('places.id'),
                          primary_key=True, nullable=False),
                      Column(
                          'amenity_id', String(60), ForeignKey('amenities.id'),
                          primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity",
                             secondary=place_amenity, viewonly=False)

    @property
    def reviews(self):
        """
        Returns the list of Review instances with place_id equals to the
        current Place.id
        """
        from models.review import Review
        return [review
                for review in storage.all(Review).values()
                if review.place_id == self.id]

    @property
    def amenities(self):
        """Getter for amenities"""
        from models.amenity import Amenity
        return [amenity
                for amenity in storage.all(Amenity).values()
                if amenity.id in self.amenity_ids]

    @amenities.setter
    def amenities(self, obj):
        """Setter for amenities"""
        from models.amenity import Amenity
        if isinstance(obj, Amenity):
            if self.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
