// Initialize the map
var map = L.map('map').setView([52.517037, 13.388860], 13);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var marker; // To keep track of the single marker
var waypoint; // Variable to store the coordinates of the waypoint

// Add marker on click
map.on('click', function(e) {
    if (marker) {
        map.removeLayer(marker); // Remove existing marker
    }
    marker = L.marker(e.latlng).addTo(map);
    map.setView(e.latlng, 13); // Center the map on the new marker
    waypoint = e.latlng;
    document.getElementById('lat').value = e.latlng.lat;
    document.getElementById('long').value = e.latlng.lng;
});

// Search for a location and add it as a waypoint
function searchLocation() {
    var searchText = document.getElementById('search').value;
    fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + searchText)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                var firstResult = data[0];
                var latLng = [firstResult.lat, firstResult.lon];

                // Remove existing marker if any
                if (marker) {
                    map.removeLayer(marker);
                }

                // Add new waypoint marker
                marker = L.marker(latLng).addTo(map).bindPopup(firstResult.display_name).openPopup();
                map.setView(latLng, 13); // Center the map on the new marker

                // Store the coordinates in waypoint variable
                waypoint = L.latLng(firstResult.lat, firstResult.lon);
                document.getElementById('lat').value = firstResult.lat;
                document.getElementById('long').value = firstResult.lon;
            } else {
                alert('Location not found');
            }
        });
}