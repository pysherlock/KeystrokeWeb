/**
 *
 */

var Username = new Array(), Password = new Array(); // records the keys that user types in

var KD_time_username = new Array(), KU_time_username = new Array();
var KD_time_pwd = new Array(), KU_time_pwd = new Array();
var Feature_Username = new Array(), Feature_Password = new Array();

var Index = -1;

function KEY(index, key, which, downtime, uptime) {
	this.index = index;
	this.key = key;
	this.which = which;
	this.time_D = downtime;
	this.time_U = uptime;
}

var keystroke = function(field, Text) {
	//Record the key which is being pressed and has been released
	var Pressed_Key = new Array(), Released_Key = new Array(); 
	var Key;
	
	$(field).keydown(function(event) {
		Index += 1;
		Key = new KEY(Index, event.key, event.which, event.timeStamp, null);
		Pressed_Key.push(Key);
		
		console.log("Press: " + Key.key);
		Text.push(event.key);
	});
	
	$(field).keyup(function(event) {
		for (i = 0; i < Pressed_Key.length; i++) {
			console.log("Pressed_Key.length: " + Pressed_Key.length + " i: " + i);
			item = Pressed_Key[i];
			
			//Look for the same key in Pressed key array and release them
			//Deal with capital keys: delete the upper key from the Pressed array
			if(item.which == event.which || item.which == event.which+32 || item.which == event.which-32) {
				item.time_U = event.timeStamp;
				console.log("Release: " + item.key);
				
				//Release the key
				//Add released key to Released array
				Released_Key.push(item);
				console.log("Released_Key");
				console.log(Released_Key);

				//Delete released key from the Pressed array
				Pressed_Key.splice(i, 1);
				console.log("Pressed_Key");
				console.log(Pressed_Key);
				
				i--; //correct the index position since Pressed array's length reduce one 
			}
		}
	});
	
	// remove Backspace and other keys that user deletes because of mistake
	var length = Released_Key.length;
	for(i = 0; i < length; i++) {
		item = Released_Key[i];
		if(item.which == 8) {
			if(i == 0) {
				Released_Key.splice(i, 1);
				length--;
				i--;
			}
			else {
				Released_Key.splice(i-1, 2);
				length-=2;
				i-=2;
			}
		}
	}
	
	//return text;
	return Released_Key;
}

var main = function () {
	
	Feature_Username = keystroke("#username", Username);
	Feature_Password = keystroke("#password", Password);
	
	$('#triger').click(function() {
		alert("Username: " + Username + " " 
				+ " \nPassword: " + Password);
	});
}

$(document).ready(main);
//$(document).ready(keystroke);

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