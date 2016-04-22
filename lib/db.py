"""
    This file controls all DB setup and session logic.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from utils import uuid

DRIVER = 'sqlite+pysqlite:///'
FULL_DB_URL = DRIVER + os.path.join(os.path.dirname(__file__),
                                    os.pardir, 'users.db')

engine = create_engine(FULL_DB_URL)
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
        return self.id

    def to_dict(self):
        '''
        Convenience method to generate a dict from a model instance.
        '''
        return_dict = {}
        for column in self.__table__.columns:
            return_dict[column.name] = getattr(self, column.name)

        return return_dict


def safe_commit():
    """ This commit function will rollback the transaction if
        committing goes awry."""
    from sqlalchemy.exc import InvalidRequestError

    try:
        session.commit()
    except InvalidRequestError as exc:
        print exc  # to the app log
    except (StandardError, SQLAlchemyError):
        session.rollback()
        raise
