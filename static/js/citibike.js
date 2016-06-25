
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
  duration: 4000,
  color: '#000000',
  trailColor: '#eee',
  trailWidth: 1,
  svgStyle: null
});
$( "#progress" ).addClass("text-center");
bar.animate(1.0);
$( "#progress" ).addClass("text-center");
function initMap(latitude, longitude) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: latitude, lng: longitude},
        zoom: 15
    });

    var marker = new google.maps.Marker({
	position: map.getCenter(),
	icon: {
	    path: google.maps.SymbolPath.CIRCLE,
	    scale: 4,
	    fillColor: "#3300CC",
	    strokeColor: "#3300CC",
	},
	map: map
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

var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
var labelIndex = 0;

function addMarker(latitude, longitude, markers) {
    // Add the marker at the clicked location, and add the next-available label
    // from the array of alphabetical characters.
    console.log(typeof(lat));
    console.log(typeof(longitude));
    var myLatlng = new google.maps.LatLng(latitude,longitude);
    var marker = new google.maps.Marker({
	position: myLatlng,
	label: labels[labelIndex++ % labels.length],
	map: map
    });
    markers.push(marker);
    return  labels[labelIndex-1];
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

function send_geo(){
    console.log(lat, lon);       
    $.getJSON($SCRIPT_ROOT + '/receive_coord', {lat: lat, lon: lon}, 
              function(data) {
		  var i = 0;
		  $.each(data.result, function() {
		      var ul0= $('<ul class="list-group">');
		      console.log(this.length)
		      $.each(this, function() {

			  let letter = addMarker(this.lat, this.lon, i ? parkMarkers: bikeMarkers);
			  ul0.append($('<li>',
				       {text: letter + ": " + this.name,
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
