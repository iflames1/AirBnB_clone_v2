#!/usr/bin/python3
""" Review module for the HBNB project """
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = 'review'
    name = Column(String(128), nullable=False)
    place_id = ""
    user_id = ""
    text = ""
