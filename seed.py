"""Utility file to seed events database"""

# Import os so that we can create db
import os
from server import app
from model import Event, User, Heart, db, connect_to_db

def load_users():
    """Seed fake users into jams db."""
    
    user1 = User(email="tmgaerlan@gmail.com", username="Trinity Gaerlan", password="password")
    user2 = User(email="dunbar.trinity@gmail.com", username="Trin Bar", password="password")
    user3 = User(email="emdunbar2016@gmail.com", username="Eileen Dunbar", password="password")
    db.session.add_all([user1, user2, user3])
    db.session.commit()

if __name__ == "__main__":
 
    # Connect the DB to an app so FlaskSQL alchemy works
  
    connect_to_db(app)

    # Create the tables
    db.create_all()

    # Add the bookmark types
    load_users()