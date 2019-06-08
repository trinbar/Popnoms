//Display map using map_center of location query
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: map_center,
  zoom: 10.5
});

let markerMap = {}

//add markers to map
geojson.features.forEach(function(marker) {
  //create an HTML element for each feature
  let popup = new mapboxgl.Popup({ offset: 25 })
    .setHTML('<a href="'+ marker.marker.event_url +'">' + marker.marker.event_name + '</a>');

  let el = document.createElement('div');
    el.className = 'marker';
    el.dataset.event_id = marker.properties.event_id;

  el.addEventListener("click", function(evt) {
  // 3. Highlight listing in sidebar (and remove highlight for all other listings)
    var activeItem = document.querySelectorAll('.event-card.active');
    if (activeItem[0]) {
      activeItem[0].classList.remove('active');
    }

    // Select the correct list item using the found index and add the active class
    var listing = document.getElementById('listing-' + evt.target.dataset.event_id);
    if (listing) {
      listing.classList.add('active')
    };
  });
  
//make a marker for each feature and add to map
let markerInstance = new mapboxgl.Marker(el);
  markerMap[marker.properties.event_id] = markerInstance

  markerInstance.setLngLat(marker.marker.coordinates)
    .setPopup(popup)
    .addTo(map);
    });

function getMarkerForEventId(event_id) {
  return geojson.features.find(function (feature) {
  return feature.properties.event_id === event_id
  })
  }

let listings = document.querySelectorAll(".event-card");

for (let i = 0; i < listings.length; i++) {
  listings[i].addEventListener("click", function(evt) {
    let eventId = evt.target.dataset.event_id;
    let marker = getMarkerForEventId(eventId);
    console.log(marker);
    flyToStore(marker);
     var activeItem = document.querySelectorAll('.event-card.active');
      if (activeItem[0]) {
        activeItem[0].classList.remove('active');
      }

  // Select the correct list item using the found index and add the active class
  var listing = document.getElementById('listing-' + eventId);
  if (listing) {
    listing.classList.add('active')
  };
})
}

function flyToStore(currentFeature) {
  map.flyTo({
  center: currentFeature.marker.coordinates,
  zoom: 15
});
  
let marker = markerMap[currentFeature.properties.event_id];
  console.log(marker);
  marker.togglePopup()
}

