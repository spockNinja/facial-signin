"""
    This file defines the db models.
"""

from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BOOLEAN, DATE, TEXT, UUID, VARCHAR
from sqlalchemy.schema import ForeignKey

from db import Base, MyBase


class User(MyBase, Base):
    __tablename__ = 'users'
    id = Column(UUID(), primary_key=True, nullable=False)
    active = Column(BOOLEAN())
    username = Column(VARCHAR(50), unique=True)
    password = Column(TEXT())
    google_id = Column(VARCHAR(50))
    email = Column(VARCHAR(256), unique=True)


class Entity(MyBase, Base):
    __tablename__ = 'entities'
    id = Column(UUID(), primary_key=True, nullable=False)
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=False)
    name = Column(VARCHAR(50))
    date_created = Column(DATE(), default=datetime.utcnow())
