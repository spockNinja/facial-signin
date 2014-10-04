""" This file contains functions like signing on and registering
    that do not require any previous authentication. """

import os
from flask import session
from passlib.hash import sha256_crypt
from postmark import PMMail

import db
from models import User
from utils import CONFIG, resp


def login(args):
    """ Confirm that a username and password match a User record in the db. """
    username = args.get('username')
    password = args.get('password')

    success = False
    message = ''

    if username and password:
        user_match = db.session.query(User)\
                               .filter(User.username == username).first()
        if user_match and sha256_crypt.verify(password, user_match.password):
            if user_match.active:
                session.update({
                    'username': user_match.username,
                    'userId': user_match.id,
                    'loggedIn': True
                })
                success = True
            else:
                message = 'Please confirm your registration before logging in'
        else:
            message = 'Login credentials invalid'
    else:
        message = 'You must provide a username and password'

    return resp(success, message)


def register(args):
    """ Assumes that frontend validation for existing usernames/emails
        is working and creates a new User entry.
        We then send a verification email."""
    new_user = User(username=args['username'],
                    email=args['email'],
                    password=sha256_crypt.encrypt(args['password']),
                    active=False)

    new_user.insert()

    site_url = CONFIG.get('app', 'url')

    verify_link = '{0}external/verify?id={1}'.format(site_url, new_user.id)

    subject = "Welcome to {0}!".format(CONFIG.get('app', 'name'))

    email_msg = '\n'.join([
        'Welcome! Your account has been created!',
        'Please click the link below to verify your email address.',
        verify_link, '', '',
        'Thank you for joining. We hope you enjoy your account.'
    ])

    email = PMMail(api_key=os.environ.get('POSTMARK_API_KEY'),
                   subject=subject,
                   sender=CONFIG.get('email', 'sender'),
                   to=new_user.email,
                   text_body=email_msg)

    email.send()

    return resp()


def checkUsername(args):
    """ Checks for existing usernames for frontend validation."""
    success = True
    message = ''

    existing_match = db.session.query(User)\
                               .filter(User.username == args['username']).all()

    if existing_match:
        success = False
        message = 'Username already in use.'

    return resp(success, message)


def checkEmail(args):
    """ Checks for existing emails for frontend validation."""
    success = True
    message = ''

    existing_match = db.session.query(User)\
                               .filter(User.email == args['email']).all()

    if existing_match:
        success = False
        message = ('Email already in use. ' +
                   'Please sign in or recover your account information')

    return resp(success, message)


def verify(args):
    """ Activates a user after they click the email link. """
    user_id = args.get('id')

    if not user_id:
        raise UserWarning("User ID missing")

    user = db.session.query(User).filter(User.id == user_id).first()

    if not user:
        raise UserWarning("No user found matching ID")

    user.active = True

    session.update({
        'username': user.username,
        'userId': user.id,
        'loggedIn': True
    })

    return 'dashboard.html'


def logout(args):
    """ Use the session to logout the user and redirect to index """
    session.pop('username', None)
    session.pop('userId', None)
    session.pop('loggedIn', None)
    return 'index.html'
