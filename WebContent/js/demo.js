/**
 *
 */

var keystroke = function () {
	//keystroke event
//	$(document).keypress(function() {
//		alert("keypress related to the whole document");
//	});
	
	$("input").keydown(function(event) {
		alert("handle for .keydown() called " + event.which);
		var keydown = event;
		console.log(keydown);
		//document.write(keydown);
		document.getElementById("output").innerHTML="keydown";
		document.getElementById("output").innerHTML=event.timeStamp;
		//
	});
	
	$("input").keyup(function(event) {
		alert("handle for .keyup() called " + event.which);
		var keyup = event;
		console.log(keyup);
		document.getElementById("output").innerHTML="keyup";

	});
	
//	$("input").keypress(function(event) {
//		alert("handle for .keypress() called " + event.which);
//	});
	
}

$(document).ready(keystroke);