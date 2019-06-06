"""Utility file to seed events database"""

# Import os so that we can create db
import os
from server import app
from model import User, Bookmark, db, connect_to_db
from faker import Faker
# from random import randint, randomchoice
# from eb_helper import get_events

def load_users():
    """Seed fake users into popnoms db."""
    
    fake_user_list = []

    for fake in range(10):
        fake = Faker()
        fake_user_list.append(fake)

    for user in fake_user_list:
        print(user)
        user = (User(email=user.email(), username=user.name(), password="password"))   
        db.session.add(user)

    db.session.commit()

# Function load_fake_bookmarks for demonstration purposes only.
def load_fake_bookmarks():
    """Seed fake bookmarks into popnoms db. Do this after seeding database and before running app."""
    pass


if __name__ == "__main__":
 
    # Connect the DB to an app so FlaskSQL alchemy works
  
    connect_to_db(app)

    # Create the tables
    db.create_all()

    # Add the bookmark types
    load_users()