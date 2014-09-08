""" This file contains functions like signing on and registering
    that do not require any previous authentication. """

import os
from flask import request, session
from passlib.hash import sha256_crypt
from postmark import PMMail

import db
from models.users import User
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
    """ Checks for existing accounts under the given username and email.
        If there are no matching usernames or emails,
        create a new User entry and send a verification email."""
    username = args['username']
    email = args['email']

    success = True
    message = ''

    existing_matches = db.session.query(User)\
                                 .filter(db.or_(User.username == username,
                                                User.email == email)).all()

    names_to_check = [u.username for u in existing_matches]
    if username in names_to_check:
        success = False
        message = 'Chosen Username already exists'

    emails_to_check = [u.email for u in existing_matches]
    if email in emails_to_check:
        success = False
        message = ('Given email already has an account. ' +
                   'Please sign in or recover your account information')

    if not success:
        return resp(success, message)

    new_user = User(username=args['username'],
                    email=args['email'],
                    password=sha256_crypt.encrypt(args['password']),
                    active=False)

    new_user.insert()

    site_url = CONFIG.get('app', 'url')

    verify_link = '{0}external/verify?id={1}'.format(site_url, new_user.id)

    subject = "Welocome to {0}!".format(CONFIG.get('app', 'name'))

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
