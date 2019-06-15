"""Popnoms server"""

# from jinja2 import StrictUndefined

from flask import (Flask, render_template, request, flash, redirect, session,
    jsonify, url_for)

from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, User, Bookmark

from eb_helper import (
    get_events, get_event_details, create_new_user, get_venue_details, 
    get_venue_coordinates, add_bookmark_to_db, get_attendees,
    get_interested)

from mb_helper import (set_map_center, set_markers)

import requests

# When we create a Flask app, it needs to know what module to scan for things
# like routes so the __name__ is required
# this instantiates an object of the class flask
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRETSECRETSECRET"

@app.route("/")
def index():
    """Index/homepage route."""

    return render_template("index.html")


@app.route("/registration_form", methods=["GET"])
def registration_form():
    """Show form for user signup."""

    return render_template("registration_form.html")


@app.route('/register', methods=["POST"])
def registration_process():
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

@app.route("/login_form")
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=["GET","POST"])
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

    flash("Logged in.")
    return redirect(f"/")


@app.route("/logout")
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

@app.route("/events", methods=["GET","POST"])
def display_events():
    """Display popup events.

        1) Get results from homepage's search form
        2) Obtain map center coordinates
        3) From venue_id's, obtain venue coordinates
    """

    #Get results from homepage's search form
    location = request.form["location"]
    start_date_kw = request.form["date_kw"]

    events = get_events(location, start_date_kw)

    #Obtain map center coordinates
    map_center = set_map_center(location)

    #Obtain list of venue_ids of events
    venue_ids = []
    for event in events:
        venue_id = event["venue_id"]
        event["venue_id"] = venue_id
        venue_ids.append(venue_id)

    #Obtain list of coordinates of events
    coordinates_list = []

    for venue_id in venue_ids:
        coordinates = get_venue_coordinates(venue_id)

        coordinates_list.append(coordinates)

    return render_template("events_2.html", 
                            events=events,
                            location=location,
                            map_center=map_center,
                            coordinates_list=coordinates_list)


@app.route("/event_details", methods=["GET","POST"])
def view_event_details():
    """Display popup event details."""

    event_id = request.args.get("event_id")
    #get_event_details returns a json string
    details = get_event_details(event_id)

    #Gets the user_id from the session
    user_id = session.get("user_id")   

    #Checks the user_id in session
    if user_id:
        #Gets the user object and username
        user_object = db.session.query(User).filter(User.user_id == user_id).one()
        username = user_object.username
        # Gets bookmark for the event if the user has already bookmarked the event and is logged in
        # Display user's bookmarks if they have already bookmarked the event
        bookmark = db.session.query(Bookmark).filter((Bookmark.user_id == user_id) & (Bookmark.event_id == event_id)).first()

         #Gets attendees of event
        attendees = get_attendees(event_id)
        interested = get_interested(event_id)

    else:
        username = "Not logged in."
        bookmark = None
        comments = None
        attendees = "Please log in to view attendee list."
        interested = "Please log in to view interested list."
    

    return render_template("event_details.html",
                            details=details,
                            username=username,
                            bookmark=bookmark,
                            attendees=attendees,
                            interested=interested)


@app.route("/bookmark_event", methods=["GET","POST"])
def bookmark_event():
    """Mark event as bookmarked and add to db."""

    event_id = request.form["event_id"]
    # Status of bookmark type "going", "interested"
    status = request.form["bookmark_type"]
    # Get user ID from session
    user_id = session.get("user_id")

    # This helper function returns either bookmark_success or bookmark_failure message
    return add_bookmark_to_db(status, event_id, user_id)


@app.route("/my_profile")
def view_profile():
    """View my profile."""

    user_id = session.get("user_id")

    #Get user's details
    user = db.session.query(User).filter(User.user_id == user_id).one()

    going_details = []
    interested_details = []

    #Create a helper for these functions!
    if user_id:

        #Get details for events bookmarked "going"
        bookmarked_going = db.session.query(Bookmark).filter((Bookmark.bookmark_type == "going") & (Bookmark.user_id == user_id)).all()
        for event in bookmarked_going:
            going_details.append(get_event_details(event.event_id))

        #Get details for events bookmarked "interested"
        bookmarked_interested = db.session.query(Bookmark).filter((Bookmark.bookmark_type == "interested") & (Bookmark.user_id == user_id)).all()
        for event in bookmarked_interested:
            interested_details.append(get_event_details(event.event_id))

        return render_template("my_profile.html",
                                going_details=going_details,
                                interested_details=interested_details,
                                user=user)

    else:
        return("Please log in to view profile.")

@app.route("/user_profile")
def view_user_profile():
    """View other user's profile."""

    user_id = request.args.get("user_id")

    going_details = []
    interested_details = []

    user = db.session.query(User).filter(User.user_id == user_id).one()

    # Get details for events bookmarked "going"
    bookmarked_going = db.session.query(Bookmark).filter((Bookmark.bookmark_type == "going") & (Bookmark.user_id == user_id)).all()
    for event in bookmarked_going:
        going_details.append(get_event_details(event.event_id))

    # Get details for events bookmarked "interested"
    bookmarked_interested = db.session.query(Bookmark).filter((Bookmark.bookmark_type == "interested") & (Bookmark.user_id == user_id)).all()
    for event in bookmarked_interested:
        interested_details.append(get_event_details(event.event_id))

    return render_template("user_profile.html", user=user,
                            going_details=going_details, interested_details=interested_details)
    
if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
