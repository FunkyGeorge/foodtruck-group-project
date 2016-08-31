var map;
var markers = [];
var userMarker;
var infowindow = new google.maps.InfoWindow();
var circle;

function initalize() {
    // Giving the map some options
    var mapOptions = {
        zoom: 12,
        center: new google.maps.LatLng(37.7749, -122.4194)
    };

    // Creating the map
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    // Create user location marker
    var icon = {
        path: "M 256,480c-84.828,0-153.6-68.157-153.6-152.228c0-84.081, 153.6-359.782, 153.6-359.782s 153.6,275.702, 153.6,359.782C 409.6,411.843, 340.828,480, 256,480z M 255.498,282.245c-26.184,0-47.401,21.043-47.401,46.981c0,25.958, 21.217,46.991, 47.401,46.991c 26.204,0, 47.421-21.033, 47.421-46.991 C 302.92,303.288, 281.702,282.245, 255.498,282.245z",
        fillColor: '#359',
        fillOpacity: 1,
        anchor: new google.maps.Point(255.498,-26.204),
        strokeWeight: 0,
        scale: .1,
        rotation: 180
    }
    userMarker = new google.maps.Marker({
        position: mapOptions["center"],
        map: map,
        title: "Your location",
        icon: icon,
        draggable: true
    })
    circle = new google.maps.Circle({
        center: userMarker.position,
        fillColor: '#004de8',
        fillOpacity: 0.25,
        map: map,
        radius: 5000,
        strokeColor: '#004de8',
        strokeOpacity: 0.75,
        strokeWeight: 1
    })
    userMarker.addListener('dragend', filterMarkers)
    // distanceCircle(userMarker.position);
}


$(document).ready(function() {
    createMarkersFromJSON();
    initalize();
    $("#filters form").on('change', function() {
        console.log("form change")
        filterMarkers();
    });

    $('.btnFeedback').click(function(){
        $('#pressed').val($(this).val())
    })

    $('form#feedbackBox').on('submit', function(e) {
        e.preventDefault();
        $.post('/feedback',$(this).serialize(), function(res){
            
        })
    })

    $('form#reviewBox').on('submit', function(e){
        e.preventDefault();
        $.post('/review',$(self).serialize(), function(res){
            
        })
    })
});

function createMarkersFromJSON() {
    $.getJSON("https://data.sfgov.org/api/views/jjew-r69b/rows.json", function(trucksjson) {
        for (var i = 0; i < trucksjson['data'].length; i++) {
            var obj = trucksjson['data'][i];
            var latlong = new google.maps.LatLng(obj[29], obj[30]);

            var marker = new google.maps.Marker({
                position: latlong,
                map: map,
                title: obj[26],
                dayOrder: obj[8],
                startTime: moment(obj[18], "HH:mm"),
                endTime: moment(obj[19], "HH:mm")
            });

            google.maps.event.addListener(marker, 'click', function(){
                infowindow.close(); // Close previously opened infowindow
                infowindow.setContent( "<div id='infowindow'>"+this.title+"<br>"+moment().to(this.endTime, true)+" left at location</div>");
                infowindow.open(map, this);

                openReviewBox(this);
            });

            markers.push(marker);
        }
        filterMarkers();
    });
}

function filterMarkers() {
    circle.setCenter(userMarker.position)
    var maxUserDistance = parseInt($("#filters form input[name='distance']").val())
    circle.setRadius(maxUserDistance)
    var time = moment($("#timepicker").val(), "hh:mm a");
    for (var i = 0; i < markers.length; i++) {
        var isDay = $('#filters form input[name=day]:radio:checked').val() == markers[i]['dayOrder'];
        var isTime = time.isBetween(markers[i]['startTime'], markers[i]['endTime']);
        var isClose =  maxUserDistance > google.maps.geometry.spherical.computeDistanceBetween(userMarker["position"], markers[i]["position"]);
        if (isDay && isTime && isClose) {
            markers[i].setVisible(true)
        } else {
            markers[i].setVisible(false)
        }
    }
}

function openReviewBox(arg) {
    console.log(arg)
    console.log(arg.title)
    $('#truck').text("Name: " + arg.title)
    $('#frmTruck').val(arg.title)
    $('#frmReview').val(arg.title)
}

// function getTruckJSON() {
//     $.getJSON("https://data.sfgov.org/api/views/jjew-r69b/rows.json", function(trucksjson) {
//         var data = trucksjson['data']
//         // console.log(data);
//         trucks = [];
//         var time = moment($("#timepicker").val(), "hh:mm a")

//         // FILTERING
//         for (var i=0; i < data.length; i++) {
//             // var day = ;
//             // var time = $('#filters form #timepicker').val();
//             // var start_time = new Date("January 1, 2000 " + data[i][18]).getTime();
//             // var end_time = new Date("January 1, 2000 " + data[i][19]).getTime();
//             // console.log(start_time)
//             // var start_time = moment(data[i][18], "HH:mm");
//             // var end_time = moment(data[i][19], "HH:mm");
//             // if (day  && )) {
//             trucks.push({
//                 'title': data[i][26],
//                 'id': i,
//                 'latitude': data[i][29],
//                 'longitude': data[i][30],
//             });
//             // }
//         }
//         // removeMarkers();
//         for (var i = 0; i < trucks.length; i++) {
//             placeMarkers(trucks[i])
//         } // end loop
//     }
//     );
// }

function placeMarkers(obj) {
    // Adding a new marker for the object
    var markerPosition = new google.maps.LatLng(obj.latitude, obj.longitude);
    var marker = new google.maps.Marker({
        position: markerPosition,
        map: map,
        title: obj.title, // this works, giving the marker a title with the correct title
        visible: false
    });
    google.maps.event.addListener(marker, 'click', function(){
        infowindow.close(); // Close previously opened infowindow
        infowindow.setContent( "<div id='infowindow'>"+marker.title+"</div>");
        infowindow.open(map, marker);
    });
    markers.push(marker);
    filterMarkers();
}

// function removeMarkers() {
//     for (var i = 0; i < markers.length; i++) {
//         markers[i].setMap(null);
//     }
//     markers = [];
// }
