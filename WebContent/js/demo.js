/**
 *
 */

var keystroke = function () {
	//keystroke event
	$("").keydown(function() {
		alert("handle for .keydown() called");
	});
}

var xTriggered = 0;
$( "#target" ).keydown(function( event ) {
  if ( event.which == 13 ) {
   event.preventDefault();
  }
  xTriggered++;
  var msg = "Handler for .keydown() called " + xTriggered + " time(s).";
  $.print( msg, "html" );
  $.print( event );
});

$( "#other" ).click(function() {
  $( "#target" ).keydown();
});

$(document).ready(keystroke);