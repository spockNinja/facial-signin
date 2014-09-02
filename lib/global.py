""" This file contains functions like signing on and registering
    that do not require any previous authentication. """

import os
from passlib.hash import sha256_crypt
from postmark import PMMail

import db
from models.users import User
from utils import CONFIG, resp, SITE_URL


def register(json_data):
    """ Checks for existing accounts under the given username and email.
        If there are no matching usernames or emails,
        create a new User entry and send a verification email."""

    existing_usernames = db.session.query(User)\
                              .filter(User.username == json_data['username'])\
                              .all()
    if existing_usernames:
        return resp(False, 'Chosen Username already exists')

    existing_emails = db.session.query(User)\
                              .filter(User.email == json_data['email']).all()
    if existing_emails:
        return resp(False, 'Given email already has an account. ' +
                           'Please sign in or recover your account information')

    new_user = User(username=json_data['username'],
                    email=json_data['email'],
                    password=sha256_crypt.encrypt(json_data['password']),
                    active=False)

    new_user.insert()

    verify_link = '{0}/verifyEmail?id={1}'.format(SITE_URL, new_user.id)

    subject = "Welocome to {0}!".format(CONFIG.get('app', 'name'))

    msg = '\n'.join([
        'Welcome! Your account has been created!',
        'Please click the link below to verify your email address.',
        verify_link, '', '',
        'Thank you for joining. We hope you enjoy your account.'
    ])

    email = PMMail(api_key=os.environ.get('POSTMARK_API_KEY'),
                   subject=subject,
                   sender=CONFIG.get('email', 'sender'),
                   to=new_user.email,
                   text_body=msg)

    email.send()
