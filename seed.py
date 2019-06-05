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

    for fake in range(300):
        fake = Faker()
        fake_user_list.append(fake)

    # add_to_db = []

    for user in fake_user_list:
        print(user)
        user = (User(email=user.email(), username=user.name(), password="password"))

    # print(add_to_db)    
        db.session.add(user)
    db.session.commit()

# def fake_helper():
#     """Helper function for load_fake_bookmarks() to create fake search queries."""

#     location = randomchoice("San Francisco, CA", "New York, NY", "Austin, TX")
#     start_date_kw = randomchoice("today", "tomorrow", "this week", "next week", "this month", "next month")

#     events = []

#     for fake in range(300):
#         fake = Faker()
#         events.append(get_events(location, start_date_kw))

#     return events

# def load_fake_bookmarks():
#     """Seed fake bookmarks into popnoms db."""

#     fake_bookmarks = []

#     for fake in range(300):
#         fake = Faker()
#         fake_bookmarks.append(fake)

#     add_to_db = []


#     for bookmark in fake_bookmarks:
#         add_to_db.append(Bookmark(bookmark_type=randint(1,2), event_id=, user_id=, timestamp=))


if __name__ == "__main__":
 
    # Connect the DB to an app so FlaskSQL alchemy works
  
    connect_to_db(app)

    # Create the tables
    db.create_all()

    # Add the bookmark types
    load_users()