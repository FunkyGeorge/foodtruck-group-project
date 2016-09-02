var map;
var markers = [];
var userMarker;
var infowindow = new google.maps.InfoWindow();
var circle;

function iconConstructor(hexcolor) {
    var icon = {
        path: "M 256,480c-84.828,0-153.6-68.157-153.6-152.228c0-84.081, 153.6-359.782, 153.6-359.782s 153.6,275.702, 153.6,359.782C 409.6,411.843, 340.828,480, 256,480z M 255.498,282.245c-26.184,0-47.401,21.043-47.401,46.981c0,25.958, 21.217,46.991, 47.401,46.991c 26.204,0, 47.421-21.033, 47.421-46.991 C 302.92,303.288, 281.702,282.245, 255.498,282.245z",
        fillColor: hexcolor,
        fillOpacity: 1,
        anchor: new google.maps.Point(255.498,-26.204),
        // strokeWeight: 1,
        // strokeColor: '#fc0',
        scale: .075,
        rotation: 180
    }
    return icon
}

function initalize() {
    // Giving the map some options
    var mapOptions = {
        zoom: 12,
        center: new google.maps.LatLng(37.7749, -122.4194)
    };

    // Creating the map
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    // Create user location marker
    userMarker = new google.maps.Marker({
        position: mapOptions["center"],
        map: map,
        title: "Your location",
        icon: iconConstructor('#359'),
        draggable: true
    })
    circle = new google.maps.Circle({
        center: userMarker.position,
        fillColor: '#004de8',
        fillOpacity: 0.25,
        map: map,
        radius: 10000,
        strokeColor: '#004de8',
        strokeOpacity: 0.75,
        strokeWeight: 1
    })
    userMarker.addListener('dragend', filterMarkers)
    // distanceCircle(userMarker.position);

    // Set today as default day
    // moment().day()
    $("#filters #day.btn-group .btn:nth-child("+(moment().day()+1)+")").addClass("active")
}


$(document).ready(function() {
    // Grab JSON data
    createMarkersFromJSON();
    // Initialize the map
    initalize();
    // Setup event listeners
    $("#filters #options input").on('change', function() {
        console.log("input change")
        filterMarkers();
    });

    $('.btnFeedback').click(function(){
        $('#pressed').val($(this).val())
    })

    $('form#favBox').on('submit', function(e) {
        var favorite = true
        e.preventDefault();
        $.post('/favorite',$(this).serialize(), function(res){

        })
        if ($('#reviewForm #favBox input[name="favorite"]').val() == 0){
            favorite = false;
        }
        checkFavorite(favorite);
    })

    $('form#reviewBox').on('submit', function(e){
        e.preventDefault();
        $.post('/review',$(this).serialize(), function(res){
            populateReviews();
            $('form#reviewBox')[0].reset();
        })
    })
    $('#filters .btn-group .btn').on('click', function() {
        $(this).siblings().removeClass("active")
        $(this).addClass("active")
        filterMarkers();
    });

    $('#filters form#reminder').on('submit', function(e) {
        e.preventDefault();
        console.log($('#filters form#reminder input[name=date]').val())
        var reminderTime = moment($('#filters form#reminder input[name=date]').val(), "LLLL")
        console.log(reminderTime.format("HH:mm:ss"))
        // Set up # of days to add to startTime
        var intDay = parseInt($('#filters #day button.active').val());
        if (moment().day() > intDay) {
            intDay += 7
        }
        if (reminderTime.isBefore()) {
            reminderTime = moment().add(20, 'seconds')
        }

        $('#filters form#reminder input[name=date]').val(reminderTime.format("YYYY-MM-DD HH:mm:ss"))
        $.post('/createReminder', $(this).serialize(), function(res) {
            $('#filters form#reminder button').removeClass("btn-primary").addClass("btn-success").html("Reminder sent!")
        })
    });
});

// Retrives JSON data, creates a map marker for each including event listeners. Pushes
// each marker object to markers array, then filters markers based on default filters.
function createMarkersFromJSON() {
    $.getJSON("https://data.sfgov.org/api/views/jjew-r69b/rows.json", function(trucksjson) {
        userFavs = $.get('/getFavs', function(favorites){
            favIcon = iconConstructor('#fc0')
            console.log(favorites['favorites']);
            console.log(trucksjson['data'][1])
            for (var i = 0; i < trucksjson['data'].length; i++) {
                var obj = trucksjson['data'][i];
                var latlong = new google.maps.LatLng(obj[29], obj[30]);


                var marker = new google.maps.Marker({
                    position: latlong,
                    map: map,
                    title: obj[26],
                    dayOrder: obj[8],
                    startTime: moment(obj[18], "HH:mm"),
                    endTime: moment(obj[19], "HH:mm"),
                    menu: obj[15],
                    location: obj[13],
                    time: obj[14],
                });

                if (favorites['favorites']) {
                    for (var j = 0; j < favorites['favorites'].length; j++) {
                        if (marker.title == favorites['favorites'][j]['name']) {
                            handleFavorites(marker)
                        }
                    }
                }
                google.maps.event.addListener(marker, 'click', function(){
                    var intDay = parseInt($('#filters #day button.active').val());
                    if (moment().day() > intDay) {
                        intDay += 7
                    }
                    this.time = moment(this.startTime, "HH:mm").day(intDay)
                    console.log(this.time.format("LLLL"))
                    if (moment().isAfter(this.time)) {
                        this.message = moment().to(this.endTime, true)+" left at location"
                    } else {
                        this.message = "Opens " + moment().calendar(this.time)
                    }
                    console.log(this.message)
                    infowindow.close(); // Close previously opened infowindow
                    infowindow.setContent( "<div id='infowindow'>"+this.title+"<br>"+ this.message +"</div>");
                    infowindow.open(map, this);

                    openReviewBox(this);
                });

                markers.push(marker);
            };
            filterMarkers();
        });
    });
}

function handleFavorites(marker) {
    if (!marker.favorite) {
        marker.setIcon(favIcon);
        marker.favorite = true;
    } else {
        marker.setIcon();
        marker.favorite = false;
    }
}

// function getFavorites() {
//     // Favorites
//     favIcon = iconConstructor('#fc0')
//     userFavs = $.get('/getFavs', function(res){
//         console.log(res['favorites']);
//         return res;
//     });
// }

// Filters markers according to the filters set on sidebar. Only allows markers that
// satisfy all filter criteria to remain visible, others are hidden.
function filterMarkers() {

    circle.setCenter(userMarker.position)
    var maxUserDistance = parseInt($("#filters input[name='distance']").val())
    circle.setRadius(maxUserDistance)
    var time = moment($("#timepicker").val(), "hh:mm a");
    for (var i = 0; i < markers.length; i++) {
        var isFavorite = false
        var isDay = $('#filters #day.btn-group .btn.active').val() == markers[i]['dayOrder'];
        var isTime = time.isBetween(markers[i]['startTime'], markers[i]['endTime']);
        var isClose =  maxUserDistance > google.maps.geometry.spherical.computeDistanceBetween(userMarker["position"], markers[i]["position"]);
        for (var j = 0; j < userFavs.length; j++) {
            if (markers[i]['title'] == userFavs[j]) {
                isFavorite = true
            }
        }
        if (isDay && isTime && isClose) {
            markers[i].setVisible(true)
            if (isFavorite) {
                markers[i].setIcon(favIcon)
            }
        } else {
            markers[i].setVisible(false)
        }
    }
}

function openReviewBox(arg) {
    $('form#reviewBox')[0].reset();
    $('#frmReview').val(arg.title)
    $('#frmFav').val(arg.title)
    $('#filters form#reminder input[name="truckName"]').val(arg.title)
    $('#reviewForm').slideDown();
    $('#reviewForm h4#truckName').html(arg.title + " <span class='label label-warning'></span>")
    $('#reviewForm #truckLocation').html(arg.location + '<br>' + arg.time)
    $('#reviewForm #menu').html(arg.menu)
    $('#filters form#reminder input[name="date"]').val(arg.startTime);
    // $('#reviewForm #reviews .review').html("""");
    $.post('/getRating',$('#reviewBox').serialize(), function(res){
        $('#reviewForm h4#truckName span.label').html(res['rating']+"/5 stars");
    })
    checkFavorite(arg.favorite);
    populateReviews()
}

function checkFavorite(favorite) {
    if (favorite == true) {
        $('#reviewForm #favBox input[name="favorite"]').val(0)
        $('#reviewForm #favBox button').removeClass("btn-success").addClass("btn-danger").html("Unfavorite")
    } else {
        $('#reviewForm #favBox input[name="favorite"]').val(1)
        $('#reviewForm #favBox button').removeClass("btn-danger").addClass("btn-success").html("Favorite")
    }
}

function populateReviews() {
    $.post('/populateReviews',$('#reviewBox').serialize(), function(res){
        $('#reviewForm #reviews .review').html(res);
    })
}
