"""
    This file defines the db models.
"""

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import BOOLEAN, TEXT, VARCHAR

from db import Base, MyBase


class User(MyBase, Base):
    __tablename__ = 'users'
    id = Column(VARCHAR(36), primary_key=True, nullable=False)
    active = Column(BOOLEAN())
    username = Column(VARCHAR(50), unique=True)
    password = Column(TEXT())
    google_id = Column(VARCHAR(50))
    email = Column(VARCHAR(256), unique=True)
    face_analysis = Column(TEXT())
