/**
 *
 */

var keystroke = function () {
	//keystroke event
//	$(document).keypress(function() {
//		alert("keypress related to the whole document");
//	});
	
	$("input").keydown(function(event) {
		var keydown = event;
		var keydown_time = keydown.timeStamp;
		console.log(keydown);

		$("input").keyup(function(event) {
			var keyup = event;
			var keyup_time = keyup.timeStamp;
			var interval = keyup_time - keydown_time;
			document.getElementById("output").innerHTML="keydown: " + keydown_time + "\n keyup_time: " + keyup_time + 
										"  interval: " + interval;

		});
//		document.getElementById("output").innerHTML="keydown: " + keydown_time + "/nkeyup_time: " + keyup_time;
	
	});
	
//	$("input").keyup(function(event) {
//		alert("handle for .keyup() called " + event.which);
//		var keyup = event;
//		console.log(keyup);
//		document.getElementById("output").innerHTML="keyup";
//
//	});
	
//	$("input").keypress(function(event) {
//		alert("handle for .keypress() called " + event.which);
//	});
	
}

$(document).ready(keystroke);