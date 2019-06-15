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
        username = user["login"]["username"]
        email = user["email"]
        password = "password"
        lrg_pic = user["picture"]["large"]
        thumb_pic = user["picture"]["thumbnail"]
        location = user["location"]["city"].title() + ", " + user["location"]["state"].title()
        join_date = user["registered"]["date"][:4]

        user_details["name"] = name
        user_details["username"] = username
        user_details["email"] = email
        user_details["password"] = password
        user_details["lrg_pic"] = lrg_pic
        user_details["thumb_pic"] = thumb_pic
        user_details["location"] = location
        user_details["join_date"] = join_date

        return user_details

def load_random_users():

    user_list = []

    for x in range(75):
        user_list.append(create_random_user())

    for user in user_list:
        user = User(email=user["email"], name=user["name"], username = user["username"],
                    password=user["password"], lrg_pic=user["lrg_pic"],
                    thumb_pic=user["thumb_pic"], location=user["location"], join_date=user["join_date"])

        db.session.add(user)

    db.session.commit()

# Function load_fake_bookmarks for demonstration purposes only.
def load_fake_bookmarks():
    """See fake bookmarks into popnoms db. Do this after seeding database and before running app."""

    timestamp = datetime.now()

    for x in range(1,15):
        bookmark = Bookmark(event_id="61524483386", user_id=x,
                              bookmark_type = "going", timestamp=timestamp)
        db.session.add(bookmark)

    for y in range(16,45):
        bookmark = Bookmark(event_id="61524483386", user_id=y,
                              bookmark_type = "interested", timestamp=timestamp)
        db.session.add(bookmark)

    db.session.commit()
                              

if __name__ == "__main__":
 
    # Connect the DB to an app so FlaskSQL alchemy works
  
    connect_to_db(app)

    # Create the tables
    db.create_all()

    # Add the bookmark types
    load_random_users()
    load_fake_bookmarks()