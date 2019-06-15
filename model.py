"""Models and database functions for PopNoms project."""
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from datetime import datetime
from dateutil import parser

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

DB_URI = "postgresql:///popnoms"

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User on Popnoms website."""

    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    name = db.Column(db.String(100), nullable=False,)
    username = db.Column(db.String(50),)
    password = db.Column(db.String(50), nullable=False,)
    email = db.Column(db.String(75), nullable=False,)
    lrg_pic = db.Column(db.String(200),)
    thumb_pic = db.Column(db.String(200),)
    location = db.Column(db.String(500),)
    join_date = db.Column(db.String(5),)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} username={self.username} email={self.email}>"


class Bookmark(db.Model):
    """Heart on Popnoms website."""

    __tablename__ = "bookmarks"
    
    bookmark_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    bookmark_type = db.Column(db.String(20), nullable=False,)
    #event_id is a string because that is the datatype in the API
    #event_id is not unique because an event can be bookmarked many times by many users (many-to-many)
    event_id = db.Column(db.String, nullable=False,)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False,)
    timestamp = db.Column(db.DateTime, nullable=False,)
    
    # Relational attributes with User class
    user = db.relationship("User", backref=db.backref("users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Bookmark bookmark_id={self.bookmark_id} bookmark_type={self.bookmark_type} event_id={self.event_id} user_id={self.user_id}>"

#May not need this Event because API calls details; keep as placeholder for future implementation
# class Event(db.Model):
#     """Event of Popnoms website."""

#     __tablename__ = "events"

#     # Define events attributes

#     # Event information
#     event_id = db.Column(db.String(50), primary_key=True,)
#     name = db.Column(db.String(100), nullable=False,)
#     eb_url = db.Column(db.String(350), nullable=False,)
  
#     # Time and Location
#     start_time_local = db.Column(db.DateTime, nullable=False,)
#     end_time_local = db.Column(db.DateTime, nullable=True,)

#     venue_id = db.Column(db.String(50), nullable=False,)
#     # venue_name = db.Column(db.String(100), nullable=False,)
#     # address = db.Column(db.String(100), nullable=False,)
#     # latitude = db.Column(db.Float, nullable=False,)
#     # longitude = db.Column(db.Float, nullable=False,)
    

    # # Relational attribute with User class
    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False,)

    # # Define relationship to user
    # user = db.relationship("User", backref=db.backref("events", order_by=event_id))


     # def __repr__(self):
     #    """Provide helpful representation when printed."""

     #    return f"<Event event_id={self.event_id} name={self.name}>"


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///popnoms'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
