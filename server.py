import sys
import os
from flask import Flask, render_template, json

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import db

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/gateway")
def gateway():
    """ Handles basic json requests """

    # First we make sure file and method have been specified
    req_file = request.args.get('file')
    req_method = request.args.get('method')
    if req_file and req_method:
        import_str = "{0}.{1}".format(req_file, req_method)
        try:
            method = __import__(import_str)
        except ImportError:
            raise UserWarning("Unable to import " + import_str)

        try:
            req_json = request.get_json(force=True)
        except:
            raise UserWarning("Unable to parse json request")

        return json.dumps(method(req_json))

    else:
        raise UserWarning("You must provide a file and method for the gateway")


@app.teardown_appcontext
def close_db_session(error):
    """ Make sure the database connection closes after each request"""
    db.session.commit()
    db.session.close()
