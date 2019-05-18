"""Models and database functions for PopNoms project."""
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

DB_URI = "postgresql:///popnoms"

db = SQLAlchemy()


##############################################################################
# Model definitions

class Event(db.Model):
    """Event of Popnoms website."""

    __tablename__ = "events"

    # Define events attributes

    # Event information
    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    name = db.Column(db.String(100), nullable=False,)
    eb_url = db.Column(db.String(350), nullable=False,)
    logo = db.Column(db.String(350), nullable=True,)

    # Time and Location
    start_time = db.Column(db.DateTime, nullable=False,)
    start_time_local = db.Column(db.DateTime, nullable=False,)
    end_time = db.Column(db.DateTime, nullable=True,)
    start_time_local = db.Column(db.DateTime, nullable=True,)

    venue_id = db.Column(db.Integer, nullable=False,)
    venue_name = db.Column(db.String(100), nullable=False,)
    address = db.Column(db.String(100), nullable=False,)
    latitude = db.Column(db.Float, nullable=False,)
    longitude = db.Column(db.Float, nullable=False,)
    

    # Relational attribute with User class
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False,)

    # Define 'nice-to-have' attributes
    capacity = db.Column(db.Integer, nullable=True,)
    is_free = db.Column(db.Boolean, nullable=True,)

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("events", order_by=event_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Event event_id={self.event_id} name={self.name}> summary={self.summary}>"

class User(db.Model):
    """User on Popnoms website."""

    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    username = db.Column(db.String(50), nullable=False,)
    password = db.Column(db.String(50), nullable=False,)
    email = db.Column(db.String(75), nullable=False,)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} username={self.username} email={self.email}>"

class Search(db.Model):
    """User on Popnoms website."""

    __tablename__ = "searches"
    
    search_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False,)
    timestamp = db.Column(db.DateTime, nullable=False,)
    search_location = db.Column(db.String(75), nullable=False)

    # Relational attributes with User and Event classes
    # user = db.relationship("User", backref=db.backref("searches", order_by=search_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Search search_id={self.search_id} user_id={self.user_id} search_location={self.search_location}>"


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///popnoms'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
