"""Utility file to seed events database"""

# Import os so that we can create db
import os
from server import app
from model import User, Bookmark, db, connect_to_db
import requests
from datetime import datetime
# from eb_helper import get_events

def create_random_user():
    """Seed fake users from RandomUsers API"""

    randomapi_url = "https://randomuser.me/api/?format=json"

    response = requests.get(randomapi_url)
    
    data = response.json()
    
    for user in data["results"]:
        user_details = {}

        name = user["name"]["first"].title() + " " + user["name"]["last"].title()
        email = user["email"]
        password = "password"
        lrg_pic = user["picture"]["large"]
        thumb_pic = user["picture"]["thumbnail"]

        user_details["name"] = name
        user_details["email"] = email
        user_details["password"] = password
        user_details["lrg_pic"] = lrg_pic
        user_details["thumb_pic"] = thumb_pic

        return user_details

def load_random_users():

    user_list = []

    for x in range(75):
        user_list.append(create_random_user())

    for user in user_list:
        user = User(email=user["email"], username=user["name"], 
                    password=user["password"], lrg_pic=user["lrg_pic"],
                    thumb_pic=user["thumb_pic"])
        db.session.add(user)

    db.session.commit()

# Function load_fake_bookmarks for demonstration purposes only.
def load_fake_bookmarks():
    """See    # timestamp = datetime.now()

    # for x in range(15):
    #     bookmark = Bookmark(event_id="58032445607", user_id=x, bookmark_type = "going", timestamp=timestamp)

    # for y in range(12):
    #     bookmark = Bookmark(event_id="58032445607", user_id=x, bookmark_type = "interested", timestamp=timestamp)d fake bookmarks into popnoms db. Do this after seeding database and before running app."""

    
    pass

if __name__ == "__main__":
 
    # Connect the DB to an app so FlaskSQL alchemy works
  
    connect_to_db(app)

    # Create the tables
    db.create_all()

    # Add the bookmark types
    load_random_users()