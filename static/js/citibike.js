
var map;
var bikeMarkers = [];
var parkMarkers = [];
var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
var labelIndex = 0;
var x = document.getElementById("p_coordinates");
var s = document.getElementById("stations");
var lat = "", lon = "";


$("#address").keyup(function(event){
    if(event.keyCode == 13){
	var address = $("#address").val();
	console.debug(address);
	console.debug(typeof(address));
	var geocoder = new google.maps.Geocoder();
	geocoder.geocode( { 'address': address}, function(results, status) {
	    if (status == google.maps.GeocoderStatus.OK) {
            lat = results[0].geometry.location.lat();
            lon = results[0].geometry.location.lng();
            refreshPosition();
	    } 
        else {
		  alert("Geocode was not successful for the following reason: " + status);
	    }
	});
    }
});




function initMap(latitude, longitude) {
    var customMapTypeId = 'custom_style';
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: latitude, lng: longitude},
        zoom: 15, 
        scrollwheel: false,
        streetViewControl: false,
        styles: [{"featureType":"administrative","stylers":[{"visibility":"off"}]},{"featureType":"poi","stylers":[{"visibility":"simplified"}]},
            {"featureType":"road","elementType":"labels","stylers":[{"visibility":"simplified"}]},{"featureType":"water","stylers":[{"visibility":"simplified"}]},
            {"featureType":"transit","stylers":[{"visibility":"simplified"}]},{"featureType":"landscape","stylers":[{"visibility":"simplified"}]},
            {"featureType":"road.highway","stylers":[{"visibility":"off"}]},{"featureType":"road.local","stylers":[{"visibility":"on"}]},
            {"featureType":"road.highway","elementType":"geometry","stylers":[{"visibility":"on"}]},{"featureType":"water","stylers":[{"color":"#84afa3"},{"lightness":52}]},
            {"stylers":[{"saturation":-17},{"gamma":0.36}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"color":"#3f518c"}]}]       
    });
    
    var marker = new google.maps.Marker({
    	position: map.getCenter(),
    	icon: {
    	    path: google.maps.SymbolPath.CIRCLE,
    	    scale: 8,
    	    fillColor: "#3366FF",
    	    fillOpacity: 1,
    	    strokeColor: "#FFFFFF",
    	    strokeWeight: 4
    	},
	   map: map
    });

    var contentString = 'My Current Location'
    var infowindow = new google.maps.InfoWindow({
          content: contentString
        });
     marker.addListener('click', function() {
          infowindow.open(map, marker);
        });

    
    document.getElementById('map').style.display="block";

    document.getElementById('progress').style.display="none";
}

function toggleVisible(enableMarkers, disableMarkers){
    len = disableMarkers.length;
    for (var i = 0; i < len; ++i){
        console.log(i, enableMarkers[i]);
        enableMarkers[i].setVisible(true);
        disableMarkers[i].setVisible(false);	
    }
}

function clearMarkers(markers){
    len = markers.length;
    for (var i = 0; i < len; ++i){
        markers[i].setMap(null);
    }
    markers = []
}

function addMarker(address, latitude, longitude, markers) {
    // Add the marker at the clicked location, and add the next-available label
    // from the array of alphabetical characters.
    console.log(address);
    console.log(typeof(lat));
    console.log(typeof(longitude));
    var myLatlng = new google.maps.LatLng(latitude,longitude);
    var marker = new google.maps.Marker({
        position: myLatlng,
        label: labels[labelIndex++ % labels.length],
        map: map
    });

    var contentString = address.num_bikes_available +' available bikes at '+address.name;
    var contentString2 = "<div style=color:#2C317A><b>"+ address.name +"</b></div> <p style='display:inline'> Bikes: " +address.num_bikes_available+ '</p> <p> Docks: '+address.num_docks_available+"</p>";
    
    var infowindow = new google.maps.InfoWindow({
          content: contentString2
    });
    prev_infowindow = false;
    marker.addListener('click', function() {
        if(prev_infowindow) {
            prev_infowindow.close();
        }
        prev_infowindow = infowindow;
        infowindow.open(map, marker);
    });

    markers.push(marker);
    return  labels[labelIndex-1];
}

function get_location(){
    lat = 0;
    lon = 0;

    if (myGeocode[0] && myGeocode[1]){
		lat = Number(myGeocode[0])
		lon = Number(myGeocode[1])
		initMap(lat, lon)
		send_geo();
    }
    else if (navigator && navigator.geolocation) {
		console.log("Getting geolocation")
        navigator.geolocation.getCurrentPosition(showPosition, displayError);
    } 
    else {
        console.log('Geolocation is not supported');
    }
}

function showPosition(position) {
    console.log("Geolocation coordinates acquired");
    lat = position.coords.latitude;
    lon = position.coords.longitude;

    initMap(lat,lon);
    send_geo();
}

function refreshPosition(){
    clearMarkers(parkMarkers);
    clearMarkers(bikeMarkers);
    $("#bikes").empty();
    $("#parking").empty();
    send_geo();
    initMap(lat,lon);
    labelIndex = 0;
}

function send_geo(){
    console.log(lat, lon);       
    $.getJSON($SCRIPT_ROOT + '/receive_coord', {lat: lat, lon: lon}, 
        function(data) {
            var i = 0;
            $.each(data.result, function() {
                var ul0= $('<ul class="list-group">');
                console.log(this.length)
                $.each(this, function() {
                    var letter = addMarker(this, this.lat, this.lon, i ? parkMarkers: bikeMarkers);
                    var table_string = (letter + ")").ljust(3) + 
                        ("B: " + this.num_bikes_available + "  D: " + this.num_docks_available).ljust(12) + " - " + this.name;
                    console.log(table_string);

                    ul0.append($('<li>',
                        {text: table_string,
                        class: 'list-group-item'})); // TODO: Add rest of content here
                });
                if (i == 0)
                $("#bikes").append(ul0);
                else
                $("#parking").append(ul0);
                i++;
            });
        toggleVisible(bikeMarkers, parkMarkers);
        }
    );
}

function displayError(){
    alert("Geolocation unavailable. Try with https.");
    x.innerHTML = "Geolocation unavailable";
}

window.onload = get_location;  