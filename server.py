import sys
import os
from flask import Flask, render_template

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import db

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')


@app.teardown_appcontext
def close_db_session(error):
    """ Make sure the database connection closes after each request"""
    db.session.commit()
    db.session.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
