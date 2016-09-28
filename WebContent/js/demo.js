/**
 *
 */

var Username = new Array(); Password = new Array(); // records the keys that user types in

var keystroke = function (field) {
	//keystroke event
	var hold_time, DDKL, UDKL, UUKL; //keystroke features: hold-down time, latency between successive keys
	var key = null, prev_key = null;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          ;
	var KD_time, prev_KD_time, KU_time, prev_KU_time;
	var Text = new Array();
	
	//Key press event
	$(field).keypress(function(event) {
		var keydown = event;
		console.log(keydown);
		
		prev_key = key;
		prev_KD_time = KD_time;
		key = keydown.key;
		KD_time = keydown.timeStamp;

		Text.push(key);
	});
	
	//Key up event
	$(field).keyup(function(event) {
		var keyup = event;
		console.log(keyup);
		prev_KU_time = KU_time;
		KU_time = keyup.timeStamp;
		console.log(prev_KU_time, KU_time);
		hold_time = KU_time - KD_time;
		
		if(prev_key != null) {
			DDKL = KD_time - prev_KD_time;
			UDKL = KU_time - prev_KD_time;
			UUKL = KU_time - prev_KU_time;
			document.getElementById("output").innerHTML="Succesive keys: " + prev_key + "," + key  
												+ " KD (hold time): " + hold_time + " DDKL: " + DDKL 
												+ " UDKL: " + UDKL + " UUKL: " + UUKL;
		}
	});
	
	return Text;
	
}

var main = function () {
	Username = keystroke("#username");
	Password = keystroke("#password");
	$('#triger').click(function() {
		alert('Username: ' + Username + " Password: " + Password);
	});
	
}

$(document).ready(main);
//$(document).ready(keystroke);