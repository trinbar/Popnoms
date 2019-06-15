"""Helper functions to parse Eventbrite API"""

from pprint import pformat
import os

import requests
from flask import request
from dateutil import parser
import pytz
from datetime import datetime
from model import User, Bookmark, db, connect_to_db


#make sure to run source secrets.sh whenever activating new virtualenv


# Global variables: Eventbrite token and URL
# Change to secrets when ready for GitHub!!!
# EVENTBRITE_TOKEN = os.getenv('EVENTBRITE_TOKEN')
EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')
EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

#### SHOULD I CREATE A HELPER FUNCTION OR KEEP IN THE REGISTER ROUTE?###
def create_new_user(name, email, password):
    """Creates a new user in the DB."""

    new_user = User(email=email, username=name, password=password)
    db.session.add(new_user)
    db.session.commit()

    return new_user

def parse_datetime(timezone, local_dt_str):
    """Takes a timezone and local datetime string and returns date and time"""

    # This takes our local dateime string and parses the string and returns a DT object without TZ
    dt_obj = parser.parse(local_dt_str)

    # This returns a timezone object
    tz = pytz.timezone(timezone)

    # Makes a new datetime object with timezone
    local_time = tz.localize(dt_obj)
    local_time = local_time.strftime('%A, %B %-d at %-I:%M%p')

    return local_time

def remove_non_ascii(text):
    """Removes non ascii charecters from string."""

    return ''.join(i for i in text if ord(i)<128)


def get_events(location, start_date_kw):
    """Gets events from Evenbrite API based on location and dates."""

    # To pass parameters through url you can use www.eventbriteapi.com/v3/events/search?variable=value&variable=value

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    # Set variable, category_id, to 110 which corresponds to Food&Drink in API
    category_id = "110"

    payload = {'location.address': location, 'start_date.keyword': start_date_kw, 
    'categories': category_id}

    response = requests.get(EVENTBRITE_URL + "events/search/", headers=headers, params=payload)

    data = response.json()

    events = []

    # Loop through events and create a dict for each event which has event details
    for event in data["events"]:
        event_details = {}

        name = event["name"]["text"]
        event_id = event["id"]
        logo = event["logo"]
        eb_url = event["url"]
        venue_id = event["venue_id"]

        # Get start/end local time and timezone to add to event details dict
        start_timezone = event["start"]["timezone"]
        start_time_local = event["start"]["local"]
        end_timezone = event["end"]["timezone"]
        end_time_local = event["end"]["local"]
        # Get start and end time in a parsed format
        start_time = parse_datetime(start_timezone, start_time_local)
        end_time = parse_datetime(end_timezone, end_time_local)
        # Add event details to the dictionary
        event_details["name"] = remove_non_ascii(name)
        event_details["event_id"] = event_id
        event_details["start_time"] = start_time
        event_details["end_time"] = end_time
        event_details["eb_url"] = eb_url
        event_details["venue_id"] = venue_id
        event_details["end_timezone"] = end_timezone

        # Check to see if logo exits, if it doesn't, set it to a default image
        if logo is not None:
            logo = logo["original"]["url"]
            event_details["logo"] = logo
     
        else:
            event_details["logo"] = "https://files.gamebanana.com/img/ico/sprays/500386c464a26.png"

        events.append(event_details)
    # Returns a list of dictionaries for each event with event details
    return events

def get_event_details(event_id):
    """Gets details about a specific event by id"""
    
    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + f"events/{event_id}/", headers=headers, verify=True)

    data = response.json()
    # Get fields back from json response

    name = data['name']['text']
    description = data['description']['text']
    eb_url = data['url']
    logo = data['logo']
    # We will return the nicely formated start and end times
    start_time = parse_datetime(data['start']['timezone'], data['start']['local'])
    end_time = parse_datetime(data['end']['timezone'], data['end']['local'])
    # We will pass timezone and local times to the front end so we can seed our events database with correct datetime format
    start_time_tz = data['start']['timezone']
    start_time_local = data['start']['local']
    end_time_tz = data['end']['timezone']
    end_time_local = data['end']['local']

    venue_id = data['venue_id']

    # Get details about a venue by id
    venue_details = get_venue_details(venue_id)

    address = venue_details["full_address"]
    venue_name = venue_details["name"]
    # longitude = venue_details["longitude"]
    # latitude = venue_details["latitude"]
    # capacity = venue_details["capacity"]

    # Checks logo for url
    if logo is not None:
        logo = logo["original"]["url"]
    
    else:
        logo = "https://www.123securityproducts.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/placeholder/default/Pho_Unavail_base.jpg"
    
    event_details = {"name": name, "event_id": event_id, "description": description, "eb_url": eb_url,
    "start_time": start_time, "start_time_local": start_time_local, "start_time_tz": start_time_tz,
    "end_time": end_time, "end_time_local": end_time_local, "end_time_tz": end_time_tz, "logo": logo,
    "address": address, "venue_id": venue_id, "venue_name": venue_name}

    return event_details

def add_bookmark_to_db(status, event_id, user_id):
    """Adds bookmarked event to database."""

    bookmark_success = f"Successfully bookmarked as {status}."
    bookmark_failure = "You must be logged in to bookmark and event."
    timestamp = datetime.now()

    # If the user is logged in
    if user_id:
        # Make a new Bookmark, passing it the user_id, event_id, and bookmarktype object, add & commit
        bookmark = Bookmark(user_id=user_id, event_id=event_id, bookmark_type=status, timestamp=timestamp)
  
        db.session.add(bookmark)
        db.session.commit()
        # Return success message
        return bookmark_success
    # If the bookmark for event already exist, we want to update the bookmark type
    else:
        return bookmark_failure

def get_venue_details(venue_id):
    """Gets information about a venue based on the venue id."""

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + f"venues/{venue_id}/", 
        headers=headers, verify=True)

    data = response.json()

    # Get fields back from the JSON response
    name = data["name"]
    address = data["address"]["address_1"]
    city = data["address"]["city"]
    region = data["address"]["region"]
    latitude = data["address"]["latitude"]
    longitude = data["address"]["longitude"]
    full_address = data["address"]["localized_address_display"]

    venue_details = {"name": name, "address": address, 'full_address': full_address, 
                     "city": city, "region": region, "latitude": latitude, "longitude":longitude}

    return venue_details

def get_venue_coordinates(venue_id):
    """Gets a venue coordinates for a list of venue_ids."""


    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + f"venues/{venue_id}/", 
            headers=headers, verify=True)

    data = response.json()

    # Get lat and long from the JSON response
    latitude = float(data["address"]["latitude"])
    longitude = float(data["address"]["longitude"])

    #Create a list of coordinates tuple objects
    coordinates = [longitude, latitude]

    return coordinates

def get_attendees(event_id):
    """Gets a list of all attendees of an event."""

    # Returns a list of bookmark objects
    bookmarks = db.session.query(Bookmark).filter((Bookmark.event_id == event_id) & (Bookmark.bookmark_type == "going")).all()

    attendees = []

    for bookmark in bookmarks:
        user = bookmark.user
        attendees.append(user)

    return attendees

def get_interested(event_id):
    """Gets a list of all interested users of an event."""
    bookmarks = db.session.query(Bookmark).filter((Bookmark.event_id == event_id) & (Bookmark.bookmark_type == "interested")).all()

    interested = []

    for bookmark in bookmarks:
        user = bookmark.user
        interested.append(user)

    return interested


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")


