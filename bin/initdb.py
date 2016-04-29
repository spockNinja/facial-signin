#!/usr/bin/env python
""" Creates the db from scratch """

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'lib'))

import db
from models import *


def init_db():
    """ Creates the database from scratch.
        DO NOT RUN ON LIVE DATA """
    db.Base.metadata.bind = db.engine
    db.Base.metadata.reflect()
    db.Base.metadata.drop_all()
    db.Base.metadata.create_all()
    db.session.commit()
    db.session.close()

if __name__ == '__main__':
    init_db()
