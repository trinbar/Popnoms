"""Popnoms server"""

# from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Event #Bookmark, BookmarkType, Comment, Search

from eb_helper import (get_events, get_event_details) 


import random

# from batched_eb_request import (get_batched_results, get_list_of_suggested_events, 
# get_suggested_event_details)


# When we create a Flask app, it needs to know what module to scan for things
# like routes so the __name__ is required
# this instantiates an object of the class flask
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRETSECRETSECRET"

# # Normally, if you use an undefined variablei n Jinja2, it fails silently
# # Fix this so that it raises an error instead
# app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage route"""

    return render_template("homepage.html")

@app.route('/login', methods=['GET', 'POST'])
def login_proccess():
    """Proccesses user and adds user to session."""

    # Get form variables
    email = request.form.get("email")
    password = request.form.get("password")

    # Check the DB to see if user exists and login matches
    user = db.session.query(User).filter((User.email == email) & (User.password == password)).first()
    # If user is in DB, add user to the session
    # Flash success message
    # Return redirect to homepage
    if user:
        session["user_id"] = user.user_id
        result = {"message": "success"}
        print("session at user id!!!!", session["user_id"])
        return jsonify(result)
    else:
        result = {"message": "Wrong username/password combo"}
        return jsonify(result)


# @app.route("/display-popups", methods=['GET'])
# def display_events():
#     """Display pop-up events on Yelp"""

#     query = request.args.get('query')
#     location = request.args.get('location')
#     distance = request.args.get('distance')
#     measurement = request.args.get('measurement')
#     sort = request.args.get('sort')
#     print(location, distance, measurement)

#     # If the required information is in the request, look for afterparties
#     if location and distance and measurement:

#         # The Eventbrite API requires the location.within value to have the
#         # distance measurement as well
#         distance = distance + measurement

#         payload = {'q': query,
#                    'location.address': location,
#                    'location.within': distance,
#                    'sort_by': sort,
#                    }

#         # For GET requests to Eventbrite's API, the token could also be sent as a
#         # URL parameter with the key 'token'
#         headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

#         response = requests.get(EVENTBRITE_URL + "events/search/",
#                                 params=payload,
#                                 headers=headers)
#         data = response.json()

#         # If the response was successful (with a status code of less than 400),
#         # use the list of events from the returned JSON for Eventbrite category ID 110
#         if response.ok:
#             events = data['events']

#         # If there was an error (status code between 400 and 600), use an empty list
#         else:
#             flash(f":( No pop-ups:{data['error_description']}")
#             events = []

#         return render_template("popups.html",
#                                data=pformat(data),
#                                results=events)

#     # If the required info isn't in the request, redirect to the search form
#     else:
#         flash("Please provide all the required information!")
#         return redirect("/")



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
