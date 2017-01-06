/**
 *
 */
function KEY(index, key, which, downtime, uptime) {
	this.index = index;
	this.key = key;
	this.which = which;
	this.time_D = downtime;
	this.time_U = uptime;
}

function PressedIndex(index) {
    this.index = index;
}

var Username_text = new Array(), Password_text = new Array(); // records the keys that user types in
//Record the key which is being pressed and has been released
var UsernamePressed_Key = new Array(), PasswordPressed_Key = new Array();
var Feature_Username = new Array(), Feature_Password = new Array();
var index_password = new PressedIndex(-1), index_username = new PressedIndex(-1);
var Key;

var keystroke = function(field, Text, Index, Pressed_Key, Released_Key) {
	//Record the key which is being pressed and has been released
	$(field).keydown(function(event) {
		Index.index += 1;
		Key = new KEY(Index.index, event.key, event.which, event.timeStamp, null);
		Pressed_Key.push(Key);
		Text.push(event.key);
	});
	
	$(field).keyup(function(event) {
		for (i = 0; i < Pressed_Key.length; i++) {
			item = Pressed_Key[i];
			
			//Look for the same key in Pressed key array and release them
			//Deal with capital keys: delete the upper key from the Pressed array
			if(item.which == event.which || item.which == event.which+32 || item.which == event.which-32) {
				item.time_U = event.timeStamp;
//				console.log("Release: " + item.key);

				//Release the key
				//Add released key to Released array
				Released_Key.push(item);
//				console.log("Released_Key");
//				console.log(Released_Key, Feature_Username, Feature_Password);

				//Delete released key from the Pressed array
				Pressed_Key.splice(i, 1);
//				console.log("Pressed_Key");
//				console.log(Pressed_Key);
				
				i--; //correct the index position since Pressed array's length reduce one 
			}
		}
	});
//	return Released_Key;
}

var main = function () {
	
	keystroke("#username", Username_text, index_username, UsernamePressed_Key, Feature_Username);
	keystroke("#password", Password_text, index_password, PasswordPressed_Key, Feature_Password);

	var connection = new WebSocket("ws://localhost:8000/websocket");
	connection.onopen = function() {
   		connection.send("Hello, world");
	};
	connection.onmessage = function (evt) {
   		alert(evt.data);
   		if(evt.data.indexOf("True") != -1){
//   		    console.log("here");
   		    document.getElementById("p1").innerHTML = "Authentication succeeded or you cracked this: " + evt.data;
   		}
   		else {
//   		    console.log("here");
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

        // Reset variables used to record keystroke
	    Feature_Password.splice(0, Feature_Password.length);
	    Feature_Username.splice(0, Feature_Username.length);
	    Username_text.splice(0, Username_text.length);
	    Password_text.splice(0, Password_text.length);
	    index_password.index = -1; index_username.index = -1;
	    console.log(index_username, index_password);
	});
}

$(document).ready(main);
