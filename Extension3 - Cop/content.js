//Keystroke code

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

var Text = new Array(); // records the keys that user types in
//Record the key which is being pressed and has been released
var PressedKey = new Array();
var Feature_Keystroke = new Array();
var PressedIndex = new PressedIndex(-1);
var Key;

var keystroke = function(field, text, pressedindex, pressed_key, released_key) {
	//Record the key which is being pressed and has been released	
	$(field).keydown(function(event) {
		pressedindex.index += 1;
		Key = new KEY(pressedindex.index, event.key, event.which, event.timeStamp, null);
		pressed_key.push(Key);
        text.push(event.key);
	});
	
	$(field).keyup(function(event) {
		for (i = 0; i < pressed_key.length; i++) {
			//console.log("Pressed_Key.length: " + Pressed_Key.length + " i: " + i);
			item = pressed_key[i];
			
			//Look for the same key in Pressed key array and release them
			//Deal with capital keys: delete the upper key from the Pressed array
			if(item.which == event.which || item.which == event.which+32 || item.which == event.which-32) {
				item.time_U = event.timeStamp;
				//console.log("Release: " + item.key);
				
				//Release the key
				//Add released key to Released array
				released_key.push(item);
				//console.log("Released_Key");
				//console.log(Released_Key);

				//Delete released key from the Pressed array
				pressed_key.splice(i, 1);
				//console.log("Pressed_Key");
				//console.log(Pressed_Key);
				
				i--; //correct the index position since Pressed array's length reduce one 
			}
		}
	});
}

//capture last click position
var position="";
$(document).click(function(event) {
	if (event.clientX<427 && event.clientY<146){
		position="Top Left";
	} 
	else if(event.clientX<427 && event.clientY>550){
		position="Bottom Left";
	}
	else if (event.clientX>883 && event.clientY<150){
		position="Top Right";
	}
	else if (event.clientX>883 && event.clientY>550){
		position="Bottom Right";
	}
});
  
//Get the last pressed character
  var key="";
 $(document).keypress(function(e){
  key=String.fromCharCode( e.which );
}); 

//Get IP and location infos from the background script
var city=""; var country_name=""; var ip=""; var latitude=""; var longitude=""; 
var region_name=""; var time_zone="";var zip_code=""; var network="";
var port = chrome.runtime.connect({name:"load"});
	port.onMessage.addListener(function(message,sender){
	if (typeof message.response2 != 'undefined') {		
		network=message.response2[0];
		city=message.response2[1];
		country_name=message.response2[2];
		ip=message.response2[3];
		latitude= message.response2[4];
		longitude=message.response2[5];
		region_name=message.response2[6];
		time_zone=message.response2[7];
		zip_code=message.response2[8];}
	});

var cpuName=""; var os=""; var batteryCharging=""; var memory=""; var storage=""; 
function myFunction(){
	port.postMessage({msg:"msg"})
	port.onMessage.addListener(function(message,sender){
	var chromeVersion = /Chrome\/([0-9.]+)/.exec(navigator.userAgent)[1];
	var removable_attached=true;
	var Now=new Date();
	var NowDate=(Now.getTime());
	var Diff=NowDate-message.response[4];
	if (Diff > 15000 ) {removable_attached=false};
	var tab_detached=true;
	var Diff2=NowDate-message.response[12];
	if (Diff2 > 15000 ) {tab_detached=false};
	var tab_closed=true;
	var Diff3=NowDate-message.response[13];
	if (Diff3 > 15000 ) {tab_closed=false};
  
	var bookmark_changed=true;
	var Diff4=NowDate-message.response[14];
	if (Diff4 > 15000 ) {bookmark_changed=false};
  
	var volume=true;
	var Diff6=NowDate-message.response[16];
	if (Diff6 > 15000 ) {volume=false};
  
	var pause=true;
	var Diff7=NowDate-message.response[17];
	if (Diff7 > 15000 ) {pause=false};
  
	var speed=true;
	var Diff8=NowDate-message.response[18];
	if (Diff8 > 15000 ) {speed=false};
  
	var mute=true;
	var Diff9=NowDate-message.response[19];
	if (Diff9 > 15000 ) {mute=false};
  
	var end=true;
	var Diff10=NowDate-message.response[22];
	if (Diff10 > 15000 ) {end=false};
  
	var seek=true;
	var Diff11=NowDate-message.response[23];
	if (Diff11 > 15000 ) {seek=false};
	
	
	var Keyevents_JSON = new Array();
	for(i = 0; i < Feature_Keystroke.length; i++) {
    var str = '{' + '"index":' + Feature_Keystroke[i].index + ',"key":' + '"' + Feature_Keystroke[i].key + '"' +
                ',"which":' + Feature_Keystroke[i].which + ',"time_D":' + Feature_Keystroke[i].time_D +
                ',"time_U":' + Feature_Keystroke[i].time_U + '}';
    if(i == 0) {
          Keyevents_JSON.push('"keystroke":[' + str);
      }
      else if(i == (Feature_Keystroke.length - 1)) {
          Keyevents_JSON.push(str+']');
      }
      else {
          Keyevents_JSON.push(str);
      }
	}

	var Keystroke_JSON = '{' + Keyevents_JSON.toString() + '}';

	//Get selected text     
	var text = "";
    if (window.getSelection) {
        text = window.getSelection().toString();}	
 
	var  data={processor:message.response[24], os:message.response[27], memory:message.response[30], chrome:chromeVersion, storage:message.response[31],locIP:network, pubIP:ip, country:country_name, region: region_name,zip:zip_code,charge:message.response[28], tabIndex:message.response[8], removable:removable_attached, transition:message.response[0], priv:message.response[5],width: message.response[6], height:message.response[7], url:message.response[9], press:presstime, zoom:message.response[10],click:position, selected:text, lastCharacter:key, detach:tab_detached, closetab:tab_closed, bookmarkChange:bookmark_changed, volumeChange:volume, volume: message.response[21],muted:mute, paused:pause, speedChange:speed, currentTime:message.response[20], ended:end, seek:seek, keystroke:Keystroke_JSON};

document.dispatchEvent(new CustomEvent('csEvent', {detail: data}));
        
// Reset keystroke variables
Feature_Keystroke.splice(0, Feature_Keystroke.length);
Text.splice(0, Text.length);
PressedIndex.index = -1;
        
});}

$(document).ready(function() { start();});
var presstime=0;
var mousedowntime;
var opentime;


function start() {
	 var element = (document.getElementsByClassName("sub"))[0];
	 if (typeof element == 'undefined') {
         keystroke("#officeIdInput", Text, PressedIndex, PressedKey, Feature_Keystroke);
         element = (document.getElementsByClassName("button"))[2];
        if (typeof element == 'undefined') {
            window.requestAnimationFrame(start);
        }else {
             //Get press time
            $(element).mousedown(function() {
              var d = new Date();
              mousedowntime = d.getTime();
            });
            $(element).mouseup(function() {
              var f = new Date();
              presstime = f.getTime() - mousedowntime;
            });
            opentime = (new Date()).getTime();
            element.addEventListener("click", myFunction, false);
            
            document.addEventListener('keypress', function (e) {
                var key = e.which || e.keyCode;
                if (key === 13) { 
                    myFunction();
                }
            });
        }  
     }
	 else {
		console.log(element);
		$(element).mousedown(function() {
          var d = new Date();
          mousedowntime = d.getTime();
        });
        $(element).mouseup(function() {
          var f = new Date();
          presstime = f.getTime() - mousedowntime;
        });
        opentime = (new Date()).getTime();
	    element.addEventListener("click", myFunction, false);
	 }
  };

