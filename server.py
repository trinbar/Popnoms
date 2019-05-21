"""Popnoms server"""

# from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Event, Search

from eb_helper import (get_events, add_event_to_db, create_new_user, get_venue_details, save_search_to_db)
from mb_helper import set_map_center

import requests

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

@app.route('/registration_form', methods=['GET'])
def registration_form():
    """Show form for user signup."""

    return render_template("registration_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    # Query the DB and make sure that the user doesn't already exist
    user = db.session.query(User).filter((User.email == email) & (User.password == password)).first()

    #If user == None, register user as new_user
    if user == None:
        new_user = create_new_user(name, email, password)
        
        #Add new_user to the session
        session["new_user"] = new_user.user_id
        flash(f"User {email} added. Please log in.")
        return redirect(f"/login_form")
    else:
        flash(f"User already exists. Please log in.")
        return redirect(f"/login_form")

@app.route('/login_form')
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['GET','POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user. Please create a new account.")
        return redirect("/registration_form")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

@app.route('/view_popnoms', methods=['GET','POST'])
def view_popups():
    """Display popup events."""

    #Request.form.get results from homepage's search for
    location = request.form["location"]
    start_date_kw = request.form["date_kw"]


    events = get_events(location, start_date_kw)

    #Obtain map center coordinates
    map_center = set_map_center(location)
    

    #Get user_id from session and save search to db
    user_id = session.get("user_id")
    #If user in session
    # if user_id:
    #     save_search_to_db(user_id=user_id, search_location=location)

    return render_template("view_popnoms.html", events=events, location=location,
                           map_center=map_center)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
