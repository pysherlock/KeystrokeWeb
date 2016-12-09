/**
 *
 */

var Username_text = new Array(), Password_text = new Array(); // records the keys that user types in

var KD_time_username = new Array(), KU_time_username = new Array();
var KD_time_pwd = new Array(), KU_time_pwd = new Array();
var Feature_Username = new Array(), Feature_Password = new Array();

var index_password = -1, index_username = -1;

function KEY(index, key, which, downtime, uptime) {
	this.index = index;
	this.key = key;
	this.which = which;
	this.time_D = downtime;
	this.time_U = uptime;
}

//Record the key which is being pressed and has been released
var Pressed_Key = new Array(), Released_Key = new Array();

var keystroke = function(field, Text, Index) {
	//Record the key which is being pressed and has been released
//	var Pressed_Key = new Array(), Released_Key = new Array();
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
	//return text;
	return Released_Key;
}

var main = function () {
	
	Feature_Username = keystroke("#username", Username_text, index_password);
	Feature_Password = keystroke("#password", Password_text, index_username);
	
	var connection = new WebSocket("ws://localhost:8000/websocket");
	connection.onopen = function() {
   		connection.send("Hello, world");
	};
	connection.onmessage = function (evt) {
   		alert(evt.data);
   		if(evt.data.indexOf("True") != -1){
   		    console.log("here");
   		    document.getElementById("p1").innerHTML = "Authentication succeeded or you cracked this: " + evt.data;
   		}
   		else {
   		    console.log("here");
            document.getElementById("p1").innerHTML = "Authentication failed. Who are you or are you injured? " + evt.data;
        }
	};
	connection.onerror = function(error) {
    	console.log('WebSocket Error ' + error.data);
    };

	$('#login').click(function() {
        document.getElementById("username-typed").value = Username_text;
    	document.getElementById("password-typed").value = Password_text;

    	username = document.getElementById("username").value;
    	password = document.getElementById("password").value;

        // Transform the format of data to JSON
        // One keyevent means one json object
		var Feature_Password_JSON = new Array(), Feature_Username_JSON = new Array();

		for(i = 0; i < Feature_Password.length; i++) {
		    var str = '{' + '"index":' + Feature_Password[i].index + ',"key":' + '"' + Feature_Password[i].key + '"' +
		                ',"which":' + Feature_Password[i].which + ',"time_D":' + Feature_Password[i].time_D +
		                ',"time_U":' + Feature_Password[i].time_U + '}';
		    if(i == 0) {
		        Feature_Password_JSON.push('"password":' + '"' + password +'"' + ',"keyevent":[' + str);
		    }
		    else if(i == (Feature_Password.length - 1)) {
		        console.log(i);
		        Feature_Password_JSON.push(str+']');
		    }
		    else {
		        Feature_Password_JSON.push(str);
		    }
		}
	    Feature_Password_JSON ='"Password":' + '{'+Feature_Password_JSON.toString()+'}';
//	    console.log(JSON.parse(Feature_Password_JSON));

		for(i = 0; i < Feature_Username.length; i++) {
		    var str = '{' + '"index":' + Feature_Username[i].index + ',"key":' + '"' + Feature_Username[i].key + '"' +
		                ',"which":' + Feature_Username[i].which + ',"time_D":' + Feature_Username[i].time_D +
		                ',"time_U":' + Feature_Username[i].time_U + '}';
		    if(i == 0) {
		        Feature_Username_JSON.push('"username":' + '"' + username +'"' + ',"keyevent":[' + str);
		    }
		    else if(i == (Feature_Username.length - 1)) {
		        Feature_Username_JSON.push(str+']');
		    }
		    else {
		        Feature_Username_JSON.push(str);
		    }
		}
		Feature_Username_JSON = '"Username":' + '{'+Feature_Username_JSON.toString()+'}';
//		console.log(JSON.parse(Feature_Username_JSON));

		// Integrate Feature_Username with Feature_Password into one json
		var Feature_JSON = new Array(Feature_Username_JSON, Feature_Password_JSON);
		Feature_JSON = '{' + Feature_JSON.toString() + '}';
		console.log(Feature_JSON);
		console.log(JSON.parse(Feature_JSON));

		var obj = JSON.parse(Feature_JSON);
		console.log(obj["Username"]["username"]);

		connection.send(Feature_JSON);

	    Released_Key.splice(0, Released_Key.length);
	    Username_text.splice(0, Username_text.length);
	    Password_text.splice(0, Password_text.length);
	});
}

$(document).ready(main);
