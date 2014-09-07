import sys
import os
from flask import Flask, json, render_template, request, Response, session

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import db
import external as external_methods

app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    """ Directs logged in users to the dashboard
        and others to the index. """

    if session.get('loggedIn'):
        return render_template('dashboard.html')
    else:
        return render_template('index.html')


@app.route("/gateway")
def gateway():
    """ Handles basic json requests.
        User must be logged in for access. """

    if not session.get('loggedIn'):
        raise UserWarning("Not Authenticated")

    # First we make sure file and method have been specified
    req_file = request.args.get('file')
    req_method = request.args.get('method')
    if req_file and req_method:
        try:
            module = __import__(req_file)
        except ImportError:
            raise UserWarning("Unable to import module: " + req_file)

        try:
            req_json = request.get_json(force=True)
        except:
            raise UserWarning("Unable to parse json request")

        method = getattr(module, req_method)
        if not method:
            raise UserWarning("No method named: " + req_method)

        result = method(req_json)

        if type(result) in [list, dict]:
            return Response(response=json.dumps(result),
                            status=200,
                            mimetype='application/json')
        else:
            return Response(response=result,
                            status=200,
                            mimetype='text/plain')

    else:
        raise UserWarning("You must provide a file and method for the gateway")


@app.route("/external/<method>", methods=['GET', 'POST'])
def external(method=None):
    """ Handles functions that do not require authentication. """

    method = getattr(external_methods, method)

    if not method:
        raise UserWarning("No external method named: " + method)

    results = method(request.args)

    if request.method == 'POST':
        return Response(response=json.dumps(results),
                        status=200,
                        mimetype='application/json')
    else:
        return render_template(results)


@app.teardown_appcontext
def close_db_session(error):
    """ Make sure the database connection closes after each request"""
    db.safe_commit()
    db.session.close()
