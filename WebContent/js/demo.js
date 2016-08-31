/**
 *
 */

var keystroke = function () {
	//keystroke event
	$(document).keypress(function() {
		alert("keypress related to the whole document");
	})
	$("input").keydown(function(event) {
		alert("handle for .keydown() called");
		$("#print-output").print("hello");
		
	});
	
	$("input").keyup(function() {
		alert("handle for .keyup() called");
	})
	
//	$("#target").keydown(function() {
//		$("#print-output").print("hello keydown");
//	});
//	
//	$("#triger").click(function() {
//		$("#target").keydown();
//		alert("hello keystroke");
//	});
	
}

$(document).ready(keystroke);
//var xTriggered = 0;
//$( "#target" ).keydown(function( event ) {
//  if ( event.which == 13 ) {
//   event.preventDefault();
//  }
//  xTriggered++;
//  var msg = "Handler for .keydown() called " + xTriggered + " time(s).";
//  $.print( msg, "html" );
//  $.print( event );
//});
//
//$( "#other" ).click(function() {
//  $( "#target" ).keydown();
//});

