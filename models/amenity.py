#!/usr/bin/python3
"""This module defines a class Amenity"""
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """This class defines an amenity by various attributes"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    """ place_amenities = relationship("Place", secondary='place_amenity',
                                   viewonly=False)
    """
