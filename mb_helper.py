"""Helper functions to parse Mapbox API"""

import os

import requests
from model import Event, User, Search, db, connect_to_db
from eb_helper import (get_events, get_venue_details)

# Forward Mapbox geocoding URL and default Mapbox token
MAPBOX_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
MAPBOX_TOKEN = "pk.eyJ1IjoidHJpbmJhciIsImEiOiJjanZ3emhpNXoxZW9kNDRwMWtzaWpwNm8xIn0.2201lSCmgIMWpQndN1igLg"

def set_map_center(location):
    """Gets locations from Mapbox API in GeoJSON based on location"""

    # Set params payload
    payload = {'limit': 2, 'access_token': MAPBOX_TOKEN}

    response = requests.get(MAPBOX_URL + location + ".json?", params=payload)

    data = response.json()

    for feature in data["features"]:
        center = feature["center"]

    return center


def set_pins(events):
    """Pins coordinates of events."""

    venue_ids = []

    for event in events:
        venue_ids.append(event["venue_id"])