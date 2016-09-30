/**
 *
 */

var Username = new Array(), Password = new Array(); // records the keys that user types in

var Pressed_KEY = new Array(), Released_KEY = new Array();

var KD_time_username = new Array(), KU_time_username = new Array();
var KD_time_pwd = new Array(), KU_time_pwd = new Array();
var Feature_Username = new Array(), Feature_PWD = new Array();

var index = -1;


var keystroke = function(field) {
	var KEY = new Object();
	var text = new Array();
	
	$(field).keydown(function(event) {
		index += 1;
		KEY.index = index;
		KEY.key = event.key;
		KEY.time_D = event.timeStamp;
		Pressed_Key.push(KEY);
		
		text.push(event.key);
	});
	
	$(field).keyup(function(event) {
		for (i = 0; i < Pressed_KEY.length(); i++) {
			item = Pressed_KEY[i];
			if(item.key == event.key) {
				item.time_U = event.timeStamp;
				Released_KEY.push(item);
				Pressed_KEY.splice(i, 1); //Release the key
			}
		}
	});
	return text;
}

/*
var keystroke = function(field, KD_time_vec, KU_time_vec) {
	//keystroke event
	var hold_time, DDKL, UDKL, UUKL; //keystroke features: hold-down time, latency between successive keys
	var key = null, prev_key = null;
	var KD_time, prev_KD_time, KU_time, prev_KU_time;
	var Text = new Array();
	
	var KEY = new Object();
	
	
	//Key press event
//	$(field).keydown(function(event) {
//		index += 1;  //index of key in the sequence
//		
//		var keydown = event;
//		console.log(keydown);
//		
//		prev_key = key;
//		prev_KD_time = KD_time;
//		KD_time = keydown.timeStamp;
//		
//		Text.push(keydown.key);
//		KD_time_vec.push(KD_time);
//		
//	});
//	
//	//Key up event
//	$(field).keyup(function(event) {
//		var keyup = event;
//		console.log(keyup);
//		prev_KU_time = KU_time;
//		KU_time = keyup.timeStamp;
//		
//		KU_time_vec.push(KU_time);
//		console.log(prev_KU_time, KU_time);
//		
////		document.getElementById("output").innerHTML= "Succesive keys: " + prev_key + "," + key 
////		+ " KD (hold time): " + hold_time + " DDKL: " + DDKL 
////		+ " UDKL: " + UDKL + " UUKL: " + UUKL;
//		
//		hold_time = KU_time - KD_time; //And this hold time is not correct
//		//feature.push(hold_time);
//		
//		if(prev_key != null) {
//			DDKL = KD_time - prev_KD_time;
//			UDKL = KU_time - prev_KD_time;
//			UUKL = KU_time - prev_KU_time; //KU_time is undefine, there is no key up before
//			//feature.push(DDKL);
//			//feature.push(UDKL);
//			//feature.push(UUKL);
//			document.getElementById("output").innerHTML="Succesive keys: " + prev_key + "," + key
//												+ " KD (hold time): " + hold_time + " DDKL: " + DDKL 
//												+ " UDKL: " + UDKL + " UUKL: " + UUKL;
//		}
//	});
	
	return Text;
}
*/

var main = function () {
//	Username = keystroke("#username", KD_time_username, KU_time_username);
//	Password = keystroke("#password", KD_time_pwd, KU_time_pwd);
//	$('#triger').click(function() {
//		alert("Username: " + Username + " feature: " + Feature_Username 
//				+ " \nPassword: " + Password + " feature: " + Feature_Pwd);
//	});
	
	
	Username = keystroke("#username");
	Password = keystroke("#password");
	
	
	$('#triger').click(function() {
		alert("Username: " + Username + " \nPassword: " + Password);
	})
}

$(document).ready(main);

//$(document).ready(keystroke);