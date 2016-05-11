import base64
import cv2
import numpy as np
import simplejson as json
import stasm
import sys
import os
from flask import (Flask, flash, jsonify, redirect,
                   render_template, request, session)
from passlib.hash import sha256_crypt
from sqlalchemy import or_

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import db
from models import User
from utils import CONFIG, send_mail
from faceInfo import FaceInfo


application = Flask(__name__)
# TODO do this with api app.register_blueprint(api)
application.secret_key = CONFIG.get('app', 'secret_key')
application.debug = True


@application.route("/")
@application.route("/dashboard")
def index():
    """ Directs logged in users to the dashboard
        and others to the index. """

    if session.get('loggedIn'):
        return render_template('dashboard.html')
    else:
        return render_template('index.html')


@application.route('/login', methods=['POST'])
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
                session['username'] = user_match.username,
                session['userId'] = user_match.id,
                session['loggedIn'] = True
                success = True
            else:
                message = 'Please confirm your registration before logging in'

            if user_match.face_analysis is not None:
                session['loggedIn'] = False
                success = False
                message = 'takePhoto'
        else:
            message = 'Login credentials invalid'
    else:
        message = 'You must provide a username and password'

    return jsonify(success=success, message=message)


@application.route('/register', methods=['POST'])
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

    verify_link = 'https://{0}/verify?id={1}'.format(site_url, new_user.id)

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


@application.route('/checkUsername', methods=['POST'])
def checkUsername():
    """ Checks for existing usernames for frontend validation."""

    username = request.args.get('username')
    existing_match = db.session.query(User)\
                               .filter(User.username == username).all()

    if existing_match:
        return jsonify(success=False, message='Username already in use.')

    return jsonify(success=True)


@application.route('/checkEmail', methods=['POST'])
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


@application.route('/verify')
def verify():
    """ Activates a user after they click the email link. """
    user_id = request.args.get('id')

    if not user_id:
        raise UserWarning("User ID missing")

    user = db.session.query(User).filter(User.id == user_id).first()

    if not user:
        raise UserWarning("No user found matching ID")

    user.active = True

    session['username'] = user.username,
    session['userId'] = user.id,
    session['loggedIn'] = True

    flash('Your account is now verified!', 'info')
    return render_template('dashboard.html')


@application.route('/logout')
def logout():
    """ Use the session to logout the user and redirect to index """
    session.pop('username', None)
    session.pop('userId', None)
    session.pop('loggedIn', None)
    flash('You have sucessfully logged out.', 'info')
    return redirect('https://' + CONFIG.get('app', 'url'))


@application.route('/analyzePhoto', methods=['POST'])
def analyzePhoto():
    """ Analyzes the photo and stores it on the user facial_analysis """
    photo = request.files['webcam']

    np_arr = np.fromstring(photo.read(), np.uint8)
    gray_img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    landmarks = stasm.search_single(gray_img)

    if len(landmarks) == 0:
        return jsonify(success=False, message="Face not found. Please try again.")

    face = FaceInfo()
    face.generateInfoFromStasm(landmarks)

    landmarks = stasm.force_points_into_image(landmarks, gray_img)
    for point in landmarks:
        gray_img[round(point[1])][round(point[0])] = 255

    comparison_photo = cv2.imencode('.jpeg', gray_img)[1]
    b64_comparison_photo = base64.encodestring(comparison_photo)

    return jsonify(data=face.getInfo(),
                   img='data:image/jpeg;base64,' + b64_comparison_photo,
                   success=True)


@application.route('/compareFace', methods=['POST'])
def compareFace():
    """ Compares given face json to session user. """
    face_data = request.get_json(force=True)

    user_id = session['userId'][0]
    user = db.session.query(User).filter(User.id == user_id).first()

    known_face = FaceInfo()
    known_face.generateInfoFromJson(user.face_analysis)

    match_face = FaceInfo()
    match_face._info = face_data

    match = known_face.isSamePerson(match_face)

    session['loggedIn'] = match

    return jsonify(success=match)


@application.route('/confirmPhoto', methods=['POST'])
def confirmPhoto():
    """ User has confirmed the photo identified facial features. Save it """
    confirmed_data = request.get_json(force=True)
    user_id = session['userId'][0]
    user = db.session.query(User).filter(User.id == user_id).first()
    user.face_analysis = json.dumps(confirmed_data)

    return jsonify(success=True, data=user.face_analysis)


@application.context_processor
def inject_globals():
    return dict(app_name=CONFIG.get('app', 'name'))


@application.teardown_appcontext
def close_db_session(error):
    """ Make sure the database connection closes after each request"""
    db.safe_commit()
    db.session.close()


if __name__ == "__main__":
    application.run()
