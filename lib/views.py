""" This module contains the routes for... all teh other things. """

from flask import Blueprint, render_template, session

import db
from models import Campaign

views = Blueprint('views', __name__)

@views.route("/campaigns")
def campaigns():
    """ Queries all of the logged in user's Campaigns
        and plugs them into the campaigns template """
    _campaigns = []
    user_campaigns = db.session.query(Campaign)\
                               .filter(Campaign.user_id == session['userId'])

    for c in user_campaigns:
        _campaigns.append(c.to_dict())

    return render_template('my/campaigns.html', campaigns=_campaigns)
