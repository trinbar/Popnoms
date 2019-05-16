"""Helper functions to parse Eventbrite API"""

from pprint import pformat
import os

import requests

from dateutil import parser
import pytz
from datetime import datetime

# Global variables: Eventbrite token and URL
# Change to secrets when ready for GitHub!!!
# EVENTBRITE_TOKEN = os.getenv('EVENTBRITE_TOKEN')
EVENTBRITE_TOKEN = "JPNZQAGVM7G4FMX2RN5A"
EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"


def create_new_user(name, email, password):
    """Creates a new user in the DB."""

    new_user = User(email=email, name=name, password=password)
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

    # local_time = local_time.ctime()

    local_time = local_time.strftime('%A, %B %-d at %-I:%M%p')

    return local_time


def get_events(location, start_date_kw):
    """Gets events from Evenbrite API based on location and dates."""

    # To pass parameters through url you can use www.eventbriteapi.com/v3/events/search?variable=value&variable=value

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    # Set variable, category_id, to 110 which corresponds to Food&Drink in API
    category_id = "110"

    payload = {'query':{'location.address': location, 'start_date.keyword': start_date_kw, 
    'categories': category_id}}

    response = requests.get(EVENTBRITE_URL + "events/search/", headers=headers, 
        verify=True, params=payload)

    data = response.json()

    events = []

    # Loop through events and create a dict for each event which has event details
    for event in data["events"]:
        event_details = {}

        name = event["name"]["text"]
        event_id = event["id"]
        logo = event["logo"]

        # Get start/end local time and timezone to add to event details dict
        start_timezone = event["start"]["timezone"]
        start_time_local = event["start"]["local"]
        end_timezone = event["end"]["timezone"]
        end_time_local = event["end"]["local"]
        # Get start and end time in a parsed format
        start_time = parse_datetime(start_timezone, start_time_local)
        end_time = parse_datetime(end_timezone, end_time_local)
        # Add event details to the dictionary
        event_details["name"] = name
        event_details["event_id"] = event_id
        event_details["start_time"] = start_time
        event_details["end_time"] = end_time

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
    """Gets details about a specific event by id, and adds event to DB."""
    
    # Get event by event id
    event = Event.query.get(event_id)
    # If we already have the event in DB return event object
    if event:
        return event

    # If not, make an API call
    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + f"events/{event_id}/", headers=headers, verify=True)

    data = response.json()
    # Get fields back from json response

    name = data['name']['text']
    description = data['description']['text']
    eb_url = data['url']
    # We will return the nicely formated start and end times
    start_time = parse_datetime(data['start']['timezone'], data['start']['local'])
    end_time = parse_datetime(data['end']['timezone'], data['end']['local'])
    # We will pass timezone and local times to the front end so we can seed our events database with correct datetime format
    start_time_tz = data['start']['timezone']
    start_time_local = data['start']['local']
    end_time_tz = data['end']['timezone']
    end_time_local = data['end']['local']

    venue_id = data['venue_id']
    logo = data['logo']
    is_free = data['is_free']

    # Get details about a venue by id
    venue_details = get_venue_details(venue_id)

    address = venue_details["full_address"]
    venue_name = venue_details["name"]
    longitude = venue_details["longitude"]
    latitude = venue_details["latitude"]
    capacity = venue_details["capacity"]

    # Checks logo for url
    if logo is not None:
        logo = logo["original"]["url"]
    
    else:
        logo = "https://www.123securityproducts.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/placeholder/default/Pho_Unavail_base.jpg"
    

 # Add event to table
    event = Event(event_id=event_id, name=name, eb_url=eb_url, logo=logo, 
        start_time=start_time, start_time_local=start_time_local, end_time=end_time,
        end_time_local=end_time_local, venue_id=venue_id, venue_name=venue_name, 
        address=address, latitude=latitude, longitude=longitude, capacity=capacity, 
        is_free=is_free)

    db.session.add(event)
    db.session.commit()

    return event

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



