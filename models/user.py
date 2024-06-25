#!/usr/bin/python3
"""This module defines a class User"""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'user'
    name = Column(String(128), nullable=False)
    email = ''
    password = ''
    first_name = ''
    last_name = ''
