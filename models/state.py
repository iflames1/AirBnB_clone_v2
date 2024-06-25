#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
import models
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if models.storage_type == "db":
        cities = relationship(
            "City", backref="state", cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            """ Getter for cities """
            return [
                city for city in models.storage.all(City).values()
                if city.state_id == self.id
                ]
