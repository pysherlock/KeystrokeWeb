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

var keystroke = function(field, Text, Index) {
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
//	var length = Released_Key.length;
//	for(i = 0; i < length; i++) {
//		item = Released_Key[i];
//		if(item.which == 8) {
//			if(i == 0) {
//				Released_Key.splice(i, 1);
//				length--;
//				i--;
//			}
//			else {
//				Released_Key.splice(i-1, 2);
//				length-=2;
//				i-=2;
//			}
//		}
//	}
	
	//return text;
	return Released_Key;
}

var exec_code = function () {
    document.getElementById("username-typed").value = Username_text;
    document.getElementById("password-typed").value = Password_text;

    username = document.getElementById("username").value;
    password = document.getElementById("password").value;

    console.log("button pressed");

}

var main = function () {
	
	Feature_Username = keystroke("#username", Username_text, index_password);
	Feature_Password = keystroke("#password", Password_text, index_username);

	
	var connection = new WebSocket("ws://localhost:8080/websocket");
	connection.onopen = function() {
   		connection.send("Hello, world");
	};
	connection.onmessage = function (evt) {
   		alert(evt.data);
	};
	connection.onerror = function(error) {
    	console.log('WebSocket Error ' + error.data);
    };


	$('#login').click(function() {
		document.getElementById("username-typed").value = Username_text;
    	document.getElementById("password-typed").value = Password_text;

    	username = document.getElementById("username").value;
    	password = document.getElementById("password").value;

		connection.send(Feature_Password.data);
	});
	
	// // Socket IO
	// var socket = io.connect('http://localhost:8080');
	// socket.on('news', function(data) {
	// 	console.log(data);
	// 	socket.emit('my other event', {my: 'data'});
	// });	

//	$('#login').click(function() {
//		alert("Username: " + Username + " " 
//				+ " \nPassword: " + Password);
//	});
}

$(document).ready(main);
