import base64
import sys
import tempfile
import os
from flask import (Flask, flash, jsonify, redirect,
                   render_template, request, session)
from passlib.hash import sha256_crypt
from sqlalchemy import or_

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import db
from models import User
from utils import analyze_photo, CONFIG, send_mail

app = Flask(__name__)
# TODO do this with api app.register_blueprint(api)
app.secret_key = CONFIG.get('app', 'secret_key')
app.debug = True


@app.route("/")
@app.route("/dashboard")
def index():
    """ Directs logged in users to the dashboard
        and others to the index. """

    if session.get('loggedIn'):
        return render_template('dashboard.html')
    else:
        google_client_id = CONFIG.get('google', 'client_id')
        return render_template('index.html', google_client_id=google_client_id)


@app.route('/login', methods=['POST'])
def login():
    """ Confirm that a username and password match a User record in the db. """
    username = request.args.get('username')
    password = request.args.get('password')

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

    return jsonify(success=success, message=message)


@app.route('/register', methods=['POST'])
def register():
    """ Registers a new user. """
    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')

    if not all([username, email, password]):
        msg = 'You must provide a username, email, and password to register.'
        return jsonify(success=False, message=msg)

    existing_accounts = db.session.query(User)\
                                  .filter(or_(User.username == username,
                                              User.email == email)).all()

    if existing_accounts:
        usernames = [u.username for u in existing_accounts]

        msg = 'There is already an account with this '
        if username in usernames:
            msg += 'username'
        else:
            msg += 'email address'
        return jsonify(success=False, message=msg)

    new_user = User(username=username, email=email, active=False,
                    password=sha256_crypt.encrypt(password))

    new_user.insert()

    site_url = CONFIG.get('app', 'url')

    verify_link = '{0}/verify?id={1}'.format(site_url, new_user.id)

    subject = "Welcome to {0}!".format(CONFIG.get('app', 'name'))

    email_msg = '\n'.join([
        'Welcome! Your account has been created!',
        'Please click the link below to verify your email address.',
        verify_link, '', '',
        'Thank you for joining. We hope you enjoy your account.'
    ])

    send_mail(new_user.email, subject, email_msg)

    return jsonify(success=True,
                   message='Please check your email to verify your account.')


@app.route('/checkUsername', methods=['POST'])
def checkUsername():
    """ Checks for existing usernames for frontend validation."""

    username = request.args.get('username')
    existing_match = db.session.query(User)\
                               .filter(User.username == username).all()

    if existing_match:
        return jsonify(success=False, message='Username already in use.')

    return jsonify(success=True)


@app.route('/checkEmail', methods=['POST'])
def checkEmail():
    """ Checks for existing emails for frontend validation."""
    email = request.args.get('email')
    existing_match = db.session.query(User)\
                               .filter(User.email == email).all()

    if existing_match:
        msg = ('Email already in use. ' +
               'Please sign in or recover your account information')
        return jsonify(success=False, message=msg)

    return jsonify(success=True)


@app.route('/verify')
def verify():
    """ Activates a user after they click the email link. """
    user_id = request.args.get('id')

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

    flash('Your account is now verified!', 'info')
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    """ Use the session to logout the user and redirect to index """
    session.pop('username', None)
    session.pop('userId', None)
    session.pop('loggedIn', None)
    flash('You have sucessfully logged out.', 'info')
    return redirect('/?logout=true')


@app.route('/analyzePhoto', methods=['POST'])
def analyzePhoto():
    """ Analyzes the photo and stores it on the user facial_analysis """
    # Store the base64 data in a temp file
    raw_data = request.stream.read()
    b64_data = raw_data.replace('data:image/jpeg;base64,', '')
    decoded = base64.b64decode(b64_data)

    with tempfile.NamedTemporaryFile(suffix='.jpeg') as temp_file:
        temp_file.write(decoded)

        # Get the analysis from the utility function
        analysis = analyze_photo(temp_file.name)

    # TODO perhaps return a b64 representation of the image
    # with the facial features on it for verification?
    return jsonify(data=analysis, success=True)


@app.context_processor
def inject_globals():
    return dict(app_name=CONFIG.get('app', 'name'))


@app.teardown_appcontext
def close_db_session(error):
    """ Make sure the database connection closes after each request"""
    db.safe_commit()
    db.session.close()


if __name__ == "__main__":
    app.run()
