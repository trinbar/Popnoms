"use strict";

  let markerMap = {}

  //add markers to map
  geojson.features.forEach(function(marker) {
      //create an HTML element for each infowindow on the marker
      let popup = new mapboxgl.Popup({ offset: 25 })
      .setHTML('<a href="'+ marker.marker.event_url +'">' + marker.marker.event_name + '</a>');

      //create marker div and set each marker to respective event_id
      let el = document.createElement('div');
      el.className = 'marker';
      el.dataset.event_id = marker.properties.event_id;

      el.addEventListener("mouseover", function(evt) {
      //Highlight media card in sidebar (and remove highlight for all other listings)
          let activeItem = document.querySelectorAll('.media.active');
              if (activeItem[0]) {
                  activeItem[0].classList.remove('active');
              }

      // Select the correct list item using the found index and add the active class
      let listing = document.getElementById('listing-' + evt.target.dataset.event_id);
          if (listing) {
          listing.classList.add('active')
          };
          listing.scrollIntoView();
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

  let listings = document.querySelectorAll(".media");

  for (let i = 0; i < listings.length; i++) {
      listings[i].addEventListener("click", function(evt) {
          let eventId = evt.target.dataset.event_id;
          let marker = getMarkerForEventId(eventId);
          flyToStore(marker);
          let activeItem = document.querySelectorAll('.media.active');
          if (activeItem[0]) {
              activeItem[0].classList.remove('active');
  }

  // Select the correct list item using the found index and add the active class
    let listing = document.getElementById('listing-' + eventId);
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
      marker.togglePopup();
  }