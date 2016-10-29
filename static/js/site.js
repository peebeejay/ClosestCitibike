//
// Toggle Buttons
//
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


//
// Event Listener to mitigate Google Chrome - Mobile Address Bar Bug
//

function ElementResize() {
    var HEIGHT_CHANGE_TOLERANCE = 150; // Approximately URL bar height in Chrome on tablet
    var element = $(this);
    var viewportHeight = $(window).height()*(1);
    
    $(window).resize(function () {
        if (Math.abs(viewportHeight - $(window).height()) > HEIGHT_CHANGE_TOLERANCE) {
            viewportHeight = $(window).height()*(1);
            update();
        }
    });
    function update() {
        element.css('height', viewportHeight*(0.8) + 'px');
    }
    update();
}

$('#map').each(ElementResize);


//
// Progress Bar
//

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


//
// LJust, RJust, Center for Results Table
//

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
