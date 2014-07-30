"""
    This file controls all DB setup and session logic.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from utils import uuid

# Make sure you change this to something secure before using it
engine = create_engine('postgresql+pypostgresql://user:password@host:port/dbname', convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)

class MyBase(object):
    """ Our Mixin class for defining declarative table models
        in SQLAlchemy. We use this class to define consistent table
        args, methods, etc."""
    __table_args__ = {'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'keep_existing': True}

    def __init__(self, **kwargs):
        """ Override default __init__, if the mapper has an id
            column and it isn't set, set it to a new uuid."""
        for k, v in kwargs.items():
            setattr(self, k, v)

        if hasattr(self, 'id') and not self.id:
            self.id = uuid()
