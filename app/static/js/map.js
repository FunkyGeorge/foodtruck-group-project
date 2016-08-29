
var map;
var markers = [];

function initalize() {
    // Giving the map some options
    var mapOptions = {
        zoom: 12,
        center: new google.maps.LatLng(37.7749, -122.4194)
    };

    // Creating the map
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    // Looping through all the entries from the JSON data

    // Adding a new click event listener for the object
    function addClicker(marker, content) {
        google.maps.event.addListener(marker, 'click', function() {

            if (infowindow) {
                infowindow.close();
            }
            infowindow = new google.maps.InfoWindow({
                content: content
            });
            infowindow.open(map, marker);

        });
    }
}

$(document).ready(function() {
    getTruckJSON();
    initalize();
    $("#filters form").on('change', function() {
        getTruckJSON();
    });
});

function getTruckJSON() {
    $.getJSON("https://data.sfgov.org/api/views/jjew-r69b/rows.json", function(trucksjson) {
        var data = trucksjson['data']
        <!-- console.log(data) -->
        trucks = [];

        // FILTERING
        for (var i=0; i < data.length; i++) {
            if ($('#filters form input[name=day]:radio:checked').val() == data[i][8]) {
                trucks.push({
                    'id': i,
                    'latitude': data[i][29],
                    'longitude': data[i][30]
                });
            }
        }
        removeMarkers();
        for (var i = 0; i < trucks.length; i++) {

            // Current object
            var obj = trucks[i];

            // Adding a new marker for the object
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(obj.latitude, obj.longitude),
                map: map,
                title: obj.title // this works, giving the marker a title with the correct title
            });
            markers.push(marker)

            // Adding a new info window for the object
            // var clicker = addClicker(marker, obj.title);

        } // end loop
    }
    );
}

function removeMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
    console.log(markers)
}



