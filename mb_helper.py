"""Helper functions to parse Mapbox API"""

import os

import requests
from model import User, Bookmark, db, connect_to_db
from eb_helper import (get_events, get_venue_details)
from mapbox import Geocoder

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

def set_markers(location):
    """Gets locations from Mapbox API in GeoJSON based on location"""

    payload = {'limit': 2, 'access_token': MAPBOX_TOKEN}

    response = requests.get(MAPBOX_URL + location + ".json?", params=payload)

    data = response.json()

    markers = []
    
    for item in data["features"]:
        marker = {}

        coordinates = item["geometry"]["coordinates"]

        marker["coordinates"] = coordinates

        markers.append(marker)

    return markers