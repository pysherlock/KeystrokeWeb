//Get video factors
var Pause=0;var Volume=0; var Speed=0; var Muted=0; var Time=0; var Vol=0; var Ended=0;var Seek=0;
chrome.runtime.onConnect.addListener(function(port2){
	port2.onMessage.addListener(function(message,sender){
		if (message.greeting != null) {
			Volume=(message.greeting);}
		if (message.greeting2 != null) {
			Pause=(message.greeting2);}
		if (message.greeting3 != null) {
			Speed=(message.greeting3);}
		if (message.greeting4 != null) {
			Muted=(message.greeting4);}
		if (message.greeting5 != null) {
			Time=(message.greeting5);}
		if (message.greeting6 != null) {
			Vol=(message.greeting6);}
		if (message.greeting7 != null) {
			Ended=(message.greeting7);}
		if (message.greeting8 != null) {
			Seek=(message.greeting8);}			
  });
});


//Get public IP and location infos
var city=""; var country_name=""; var ip=""; var latitude=""; var longitude=""; 
var region_name=""; var time_zone=""; var zip_code=""; var network="";
function getPublicIp(){
	geoip = function(data){
		if (data.region_name.length > 0) {
			city=data.city;
			country_name=data.country_name;
			ip=data.ip;
			latitude=data.latitude;
			longitude=data.longitude;
			region_name=data.region_name;
			time_zone=data.time_zone;
			zip_code=data.zip_code;
		}
	}
	var el = document.createElement('script');
	el.src = 'https://freegeoip.net/json/?callback=geoip';
	document.body.appendChild(el);
}


//Get local IP 
function getLocalIPs(callback) {
	var ips = [];
	var RTCPeerConnection = window.RTCPeerConnection ||
	window.webkitRTCPeerConnection || window.mozRTCPeerConnection;
	var pc = new RTCPeerConnection({
		iceServers: []
    });
    pc.createDataChannel('');
    pc.onicecandidate = function(e) {
		if (!e.candidate) { 
		pc.close();
		callback(ips);
		return;
		}
		var ip = /^candidate:.+ (\S+) \d+ typ/.exec(e.candidate.candidate)[1];
		if (ips.indexOf(ip) == -1) 
		ips.push(ip);
		};
		pc.createOffer(function(sdp) {
		pc.setLocalDescription(sdp);
		}, function onerror() {});
}


//Get transition type
  var transitionType="";
  chrome.webNavigation.onCommitted.addListener(function(historyInfo){   
	transitionType = historyInfo.transitionType;
  });
  
 
//Get the time of tab removal
  var remove_tab=0;
  chrome.tabs.onRemoved.addListener(function (removeInfo){
    remove=new Date();
    remove_tab=(remove.getTime());   
  });
  
//Get the time of storage device attachment
  var storage_attached=0;
  chrome.system.storage.onAttached.addListener(function(storageInfo){
    d=new Date();
    storage_attached=(d.getTime());   
  });
  
//Get the time of tab detachment
  var detach_tab=0;
  chrome.tabs.onDetached.addListener(function (detachInfo){
    detach=new Date();
    detach_tab=(detach.getTime());   
  });
  
   
  
//Get the time of bookmark change
  var bookmark_changed=0;
  var new_bookmark_name="";
  chrome.bookmarks.onChanged.addListener(function (id,bookmarkInfo){
    bookm=new Date();
    bookmark_changed=(bookm.getTime());   
	new_bookmark_name=JSON.stringify(bookmarkInfo.title)
  });
  

//Get page zoom level
  var zoom=0;
  chrome.tabs.onZoomChange.addListener(function(zoomInfo){   
    zoom = zoomInfo.newZoomFactor;  
  });
  
  
  chrome.runtime.onConnect.addListener(function(port){
    getPublicIp(); 
    getLocalIPs(function(ips) { 
    network=(document.body.textContent = ips.join('\n '));
  });
  
  function verif () {
     if (country_name=="" || network=="") {
       setTimeout(verif, 100); 
     }
	 else	{
		 collected_data=[network, city,country_name, ip, latitude, longitude,region_name, time_zone, zip_code];
	     port.postMessage({response2:collected_data})
	 }		 
    }
  	
  verif();	

  port.onMessage.addListener(function(message,sender){

//Get storage device infos
  var storage="";
  chrome.system.storage.getInfo(function(storageInfo){
          storage = storageInfo[0].name.replace(/\0/g,'') + '-' + storageInfo[0].type + '-' + JSON.stringify(storageInfo[0].capacity);
  });


//Get CPU infos
  var cpuName="";
  var numProcessors=0;
  chrome.system.cpu.getInfo(function(info){      
    cpuName = info.modelName;
    numProcessors = info.numOfProcessors;
  });
  

//Get memory infos
  var memory="";
  var used_memory="";
  chrome.system.memory.getInfo(function(memoryinfo){      
    memory = JSON.stringify(memoryinfo.capacity);
    available_memory = JSON.stringify(memoryinfo.availableCapacity);
    used_memory=(1-available_memory/memory)*100;
  });

//Get Operating System infos	
  var os="";
  chrome.runtime.getPlatformInfo(function(info) {    
    os=info.os;	
  });
  
//Get battery infos
  var batteryCharging=false;
  var batteryLevel=0;
  var chargingTime="";
  navigator.getBattery().then(function(batteryManager) {
    batteryCharging=(batteryManager.charging);
	batteryLev=JSON.stringify(batteryManager.level);
	batteryLevel=batteryLev*100;
    chargingTime=JSON.stringify(batteryManager.chargingTime);	
  });  
  //Get the 3 most visited websites
  var url="";
  chrome.topSites.get(function(topSites){
    for (i = 0; i <  3; i++){
      url = url + JSON.stringify(topSites[i].url) + "\n\n";
    }
  });
  
  
  //Get web history
  var histories="";
  chrome.history.search({text: '', maxResults: 3}, function(historyData){   
	for (i = 0; i <  3; i++){
      histories = histories + JSON.stringify(historyData[i].url) + "\n\n";
	}
  });
  
  //Get installed extensions
  var extensions="";
  chrome.management.getAll(function(extensionInfo){   
	  for (i = 0; i <  extensionInfo.length; i++){
      extensions = extensions + JSON.stringify(extensionInfo[i].name) + "\n\n";
	  }
  });
  

  //Get tab index, dimensions and private navigation mode 
  var incognito=false;
  var tabWidth=0;
  var tabHeight=0;
  var tabIndex=1000; 
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {  
    incognito=tabs[0].incognito;
	tabWidth=tabs[0].width;
	tabHeight=tabs[0].height;
	tabIndex=tabs[0].index;	
  });
  
    //Get opened urls
  var openedUrls ="";
  chrome.tabs.query({}, function(tabs){
	for (var i = 0; i < tabs.length; i++) {
	  if (i==tabIndex) {openedUrls = openedUrls + "Login Page" + " Muted: " + (tabs[i].mutedInfo.muted) + "/  /";}
	  else{
	  openedUrls = openedUrls + (tabs[i].url) + " Muted: " + (tabs[i].mutedInfo.muted) + "/  /";  } 
    }

	openedUrls=decodeURIComponent(openedUrls);
	openedUrls=openedUrls.replace(/&/g,'');
	openedUrls=openedUrls.replace(/\+/g,'');

  });



  
  //Get the list of bookmarks
  var bookmark_list="";
  chrome.bookmarks.getTree(function(itemTree){
    itemTree.forEach(function(item){
        processNode(item);
    });
  });

  function processNode(node) {
    if(node.children) {
        node.children.forEach(function(child) { processNode(child); });
    }
    if(node.url) { bookmark_list=bookmark_list+(node.url) + "\n"; }
  }


  setTimeout(function(){
	      all_data=[transitionType, histories, url, extensions, storage_attached, incognito, tabWidth, tabHeight, tabIndex, openedUrls,zoom, bookmark_list, detach_tab, remove_tab, bookmark_changed, new_bookmark_name, Volume, Pause, Speed, Muted, Time, Vol,Ended, Seek, cpuName, numProcessors,used_memory,os,batteryCharging, batteryLevel, memory, storage];
          port.postMessage({response:all_data});
    }, 10);
}); 
});

