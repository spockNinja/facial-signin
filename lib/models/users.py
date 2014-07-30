"""
    This file defines models relating to users.
"""

from sqlalchemy import Column, String, Text

from db import Base, MyBase

class User(MyBase, Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, nullable=False)
    username = Column(String(50), unique=True)
    password = Column(Text())
    email = Column(String(256), unique=True)
