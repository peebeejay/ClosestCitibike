
$("#bikebutton").click(function(){
    console.log("bike button");
    document.getElementById("bikes").style.display = "block";
    document.getElementById("parking").style.display = "none";
    toggleVisible(bikeMarkers, parkMarkers);

});
$("#parkbutton").click(function(){
    console.log("park button");
    document.getElementById("parking").style.display = "block";
    document.getElementById("bikes").style.display = "none";    
    toggleVisible(parkMarkers, bikeMarkers);
});

var map;
var bikeMarkers = [];
var parkMarkers = [];
var bar = new ProgressBar.Circle("#progress", {
  strokeWidth: 6,
  easing: 'easeInOut',
  duration: 1000,
  color: '#000000',
  trailColor: '#30A4EF',
  trailWidth: 1,
  svgStyle: null
});
bar.animate(1)
setTimeout(function() {
    bar.animate(0.25);
}, 1000);

setTimeout(function() {
    bar.animate(1.0);
}, 2000);

setTimeout(function() {
    bar.animate(.5);
}, 3000);

setTimeout(function() {
    bar.animate(1.0);
}, 4000);

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
	    } else {
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

    styles: [   {   "stylers":[ {"visibility":"on"},    {"saturation":-100},    {"gamma":0.54}  ]   },{ "featureType":"road",   "elementType":"labels.icon",    
        "stylers":[ {"visibility":"off"}    ]   },{ "featureType":"water",  "stylers":[ {"color":"#4d4946"} ]   },{ "featureType":"poi",    "elementType":"labels.icon",
        "stylers":[ {"visibility":"off"}    ]   },{ "featureType":"poi",    "elementType":"labels.text",    "stylers":[ {"visibility":"simplified"} ]   },
        { "featureType":"road",   "elementType":"geometry.fill",  "stylers":[ {"color":"#ffffff"} ]   },{ "featureType":"road.local", "elementType":"labels.text",
        "stylers":[ {"visibility":"simplified"} ]   },{ "featureType":"water",  "elementType":"labels.text.fill",   "stylers":[ {"color":"#ffffff"} ]   },
        { "featureType":"transit.line",   "elementType":"geometry",   "stylers":[ {"gamma":0.48}  ]   },{ "featureType":"transit.station",    
        "elementType":"labels.icon",    "stylers":[ {"visibility":"off"}    ]   },{ "featureType":"road",   "elementType":"geometry.stroke",   
        "stylers":[ {"gamma":7.18}  ]   }   ]
        
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

function toggleVisible(enableMarkers, disableMarkers)
{
    len = disableMarkers.length;
    for (var i = 0; i < len; ++i)
    {
	console.log(i, enableMarkers[i]);
	enableMarkers[i].setVisible(true);
	disableMarkers[i].setVisible(false);	
    }
}

function clearMarkers(markers)
{
    len = markers.length;
    for (var i = 0; i < len; ++i)
    {
	markers[i].setMap(null);
    }
    markers = []
}

var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
var labelIndex = 0;

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
    var contentString2 = "<div style=color:#2C317A>"+ address.name +"</div> <p style='display:inline'> Available Bikes: " +address.num_bikes_available+ '</p> <p>Available Docks: '+address.num_docks_available+"</p>";
    
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

String.prototype.ljust = function( width, padding ) {
    padding = padding || " ";
    padding = padding.substr( 0, 1 );
    if( this.length < width )
        return this + padding.repeat( width - this.length );
    else
        return this;
}
String.prototype.rjust = function( width, padding ) {
    padding = padding || " ";
    padding = padding.substr( 0, 1 );
    if( this.length < width )
        return padding.repeat( width - this.length ) + this;
    else
        return this;
}
String.prototype.center = function( width, padding ) {
    padding = padding || " ";
    padding = padding.substr( 0, 1 );
    if( this.length < width ) {
        var len     = width - this.length;
        var remain  = ( len % 2 == 0 ) ? "" : padding;
        var pads    = padding.repeat( parseInt( len / 2 ) );
        return pads + this + pads + remain;
    }
    else
        return this;
}


var x = document.getElementById("p_coordinates");
var s = document.getElementById("stations");
var lat = "", lon = "";

function get_location(){
    if (navigator && navigator.geolocation) {
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
    initMap(lat,lon)
    send_geo();
}

function refreshPosition()
{
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
                    let letter = addMarker(this, this.lat, this.lon, i ? parkMarkers: bikeMarkers);
                    var table_string = (letter + ")").ljust(3) + 
                        ("B: " + this.num_bikes_available + "  D: " + this.num_docks_available).ljust(12) + " - " + this.name;
                    console.log(table_string);
                    // text: letter.ljust(10) + ": " + this.name + "- B:" + this.num_bikes_available + "  D:" + this.num_docks_available,

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
			      // var li0= $('<li>', {text: this.title});
			      // var ul1= $('<ul>');
			      // $.each(data.result, function() {
			      // 	  ul1.append($('<li>', {id: 'foo_'+this.title})
			      // 		     .append($('<a>', {href: this.link, text: this.text})
			      // 			     .append($('<strong>', {text: this.data0}))
			      // 			     .append($('<span>', {text: this.data1}))
			      // 			     .append($('<em>', {text: this.data2}))
			      // 			    )
			      // 		    );
			      // });
			      // li0.append(ul1);
			      // ul0.append(li0);
			  // });
			  // var str1 = "";
			  // var headers = ["<b>Bikes Available - 2 minimum</b>", "<b>Docks Available - 2 minimum</b>"];
			  // for (i=0; i<data.result.length; i++){
                    	  //     str1 += headers[i] + "<br>";
                    	  //     for (j=0; j<data.result[i].length; j++){
                    	  // 	  str1 += ("<b>" + (j+1) + ": " + data.result[i][j].name + "</b> |||  Distance: " + ((data.result[i][j].magnitude)*69).toFixed(2) + " mi  || Bikes: " + data.result[i][j].num_bikes_available + " |  Docks: " + data.result[i][j].num_docks_available+ "<br>");
                    	  //     }
                    	  //     str1 += "<br><br>";                   	
			  // }
			  // console.log(str1);
			  // stations.innerHTML = str1;


       

        /* //The function below is usable with Flask: request.args.get('key', default value, type=type)
        function send_geo(){ 
            $.getJSON($SCRIPT_ROOT + '/receive_coord', {
                lat: lat,
                lon: lon
                }, 

                function(data) {
                    //$("#result").text(data.result);
                    console.log(data.result);
            });
        }*/ 

        /* // The function below is an outdated version of send_geo that uses an AJAX POST method to send geolocation coordinates to the server
           // To use this function, use the following in Flask: lat = request.json['lat']  ; # lon = request.json['lon']
        	function send_geo(){
            console.log(lat);
            console.log(lon);

            $.ajax({
            url: ($SCRIPT_ROOT + '/receive_coord'),
            data: JSON.stringify({"lat": lat, "lon": lon}, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            type: "POST",
            success: function(response) {
                console.log("success:");
            },
            error: function(error) {
                console.log("error");
            }
            });
        }*/
