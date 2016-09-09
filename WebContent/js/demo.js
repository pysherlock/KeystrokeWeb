/**
 *
 */

var keystroke = function () {
	//keystroke event
	
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
	
}

$(document).ready(keystroke);