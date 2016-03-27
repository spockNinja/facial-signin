#!/usr/bin/env python
""" Creates the db from scratch """

import argparse
import sh
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'lib'))

import db
from utils import CONFIG
from models import *


def create_user_and_db():
    """ Creates the database and user in app.cfg.
        Assumes that postgres is fresh with initial users/permissions.
        ONLY FOR DEVELOPMENT PURPOSES. aws handles this for us in RDS creation."""
    username = CONFIG.get('database', 'username')
    password = CONFIG.get('database', 'password')
    db_name = CONFIG.get('database', 'name')

    def run_cmd(cmd):
        sh.psql('-c', cmd, 'postgres')

    create_user = "CREATE USER {0} WITH SUPERUSER CREATEDB PASSWORD '{1}';".format(username, password)
    run_cmd(create_user)

    create_db = "CREATE DATABASE {0} WITH OWNER {1}".format(db_name, username)
    run_cmd(create_db)


def init_db():
    """ Creates the database from scratch.
        DO NOT RUN ON LIVE DATA """
    db.Base.metadata.bind = db.engine
    db.Base.metadata.reflect()
    db.Base.metadata.drop_all()
    db.session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    db.Base.metadata.create_all()
    db.session.commit()
    db.session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize the database.')
    parser.add_argument('-f', '--first-time', dest='first_time', action='store_true')
    args = parser.parse_args()

    if args.first_time:
        create_user_and_db()

    init_db()
