# PopNoms
PopNoms is a  pop-up dining event finder that will find event listings and renders the event location on a map using Eventbrite and Mapbox APIs.

# About the Developer
PopNoms was created by Trinity Dunbar, a fellow at Hackbright Academy. 
[View LinkedIn Profile](https://www.linkedin.com/in/trinity-dunbar).

# Tech Stack
Python3, JavaScript (jQuery, AJAX), HTML/CSS, PostgreSQL, SQLAlchemy

# Features
<h3>Homepage</h3>
```
![Homepage demo](demo/READme_1.gif)
```
From the homepage users can sign up and sign in from the navigation bar, and can search pop-up dining events in any city within the next month.

<h3>Event Listings</h3>
```
![Event listings demo](demo/READme_2.gif)
```
This will take them to an event listing page where users can view the listings on the left-hand sidebar and their locations on a map. As a user hovers their cursor over a map marker, the sidebar will scroll to the event and the event card will be highlighted. To view details of the event, users can either click on the URL in the map marker's info window or on the event's logo inside of the event card.

<h3>Event Details</h3>
<img src="/demo/READme_3.gif" style="width: 150px; height: 100px;>
From the event details page, users can
<ul>
  <li>Read the event description</li>
  <li>Bookmark event as "I'm Going!" or "Interested"</li>
  <li>Share to their social media accounts on Facebook and/or Twitter</li>
  <li>Purchase tickets from Eventbrite</li>
  <li>View other PopNom users who intend on going or are interested</li>
</ul>

<h3>User Profile</h3>
```
![Profile demo](demo/READme_4.gif)
```
Once an event is bookmarked, the bookmarked event will appear in their profile.

# Set Up/Installation
* PostgreSQL
* Python3
* Eventbrite API Key

To run locally on your machine, follow these steps.

1. Clone the repository
```
$ git clone https://github.com/trinbar/Popnoms
```

2. Create a virtual environment
```
$virtualenv env
```

3. Install requirements
```
pip3 install -r requirements.txt
```

4. Retrieve an Eventbrite API 🔑 by signing up for an account.<br>
  Save them to a secrets file - DO NOT SHARE THIS! - and be sure to export.<br>
  In the file(s) you need the API 🔑 be sure to import os so you can use the key.<br><br>
  
  In the secrets file:
  ```
  export EVENTBRITE_TOKEN = "token"
  ```

  In the file(s) you will call the API 🔑:
  ```
  EVENTBRITE_TOKEN = os.environ.get("EVENTBRITE_TOKEN")
  ```
  
  5. Create a database
  ```
  $ createdb popnoms
  ```
  
  6. Seed your database
  ```
  $ python3 seed.py
  ```
  
  Now you are ready to run the app from your command line.
  ```
  $ python3 server.py
  ```
