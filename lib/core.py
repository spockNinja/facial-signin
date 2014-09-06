""" Functions that don't really fit anywhere else... """

from flask import redirect, session


def logout(empty_json):
    """ Use the session to logout the user and redirect to index """
    session.pop('username', None)
    session.pop('userId', None)
    session.pop('loggedIn', None)
    return redirect('/index.html')
