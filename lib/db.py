"""
    This file controls all DB setup and session logic.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from utils import uuid

# Heroku gives us the db url in an ENV variable
# Make sure you change the default to something secure before using it
DB_URL = os.environ.get('DATABASE_URL')
DRIVER = 'postgresql+psycopg2:'

db_url_parts = DB_URL.split(':', 1)
FULL_DB_URL = DRIVER + db_url_parts[1]

engine = create_engine(FULL_DB_URL, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()


class MyBase(object):
    """ Our Mixin class for defining declarative table models
        in SQLAlchemy. We use this class to define consistent table
        args, methods, etc."""

    def __init__(self, **kwargs):
        """ Override default __init__, if the mapper has an id
            column and it isn't set, set it to a new uuid."""
        for k, v in kwargs.items():
            setattr(self, k, v)

        if hasattr(self, 'id') and not self.id:
            self.id = uuid()

    def insert(self):
        """Convenience method to add a model to the session
        and ultimately insert in the database permanently upon commit."""
        session.add(self)
        session.merge(self)
        return self.id
