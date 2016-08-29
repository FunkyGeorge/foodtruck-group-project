
var map;
var markers = [];
var infowindow = new google.maps.InfoWindow(); /* SINGLE */

function initalize() {
    // Giving the map some options
    var mapOptions = {
        zoom: 12,
        center: new google.maps.LatLng(37.7749, -122.4194)
    };

    // Creating the map
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
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
        console.log(data);
        trucks = [];

        // FILTERING
        for (var i=0; i < data.length; i++) {
            if ($('#filters form input[name=day]:radio:checked').val() == data[i][8]) {
                trucks.push({
                    'title': data[i][26],
                    'id': i,
                    'latitude': data[i][29],
                    'longitude': data[i][30]
                });
            }
        }
        removeMarkers();
        for (var i = 0; i < trucks.length; i++) {
            placeMarkers(trucks[i])
        } // end loop
    }
    );
}

function placeMarkers(obj) {
            var markerPosition = new google.maps.LatLng(obj.latitude, obj.longitude);
            // Adding a new marker for the object
            var marker = new google.maps.Marker({
                position: markerPosition,
                map: map,
                title: obj.title // this works, giving the marker a title with the correct title
            });
            google.maps.event.addListener(marker, 'click', function(){
                infowindow.close(); // Close previously opened infowindow
                infowindow.setContent( "<div id='infowindow'>"+marker.title+"</div>");
                infowindow.open(map, marker);
            });
            markers.push(marker)
}

function removeMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}



