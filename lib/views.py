""" This module contains the routes for... all teh other things. """

from flask import Blueprint, render_template, session

import db
from models import Entity

views = Blueprint('views', __name__)


@views.route("/other")
def other():
    """ Queries all of the logged in user's Campaigns
        and plugs them into the campaigns template """
    entities = db.session.query(Entity)

    entities = [e.to_dict() for e in entities]

    return render_template('other.html', entities=entities)
