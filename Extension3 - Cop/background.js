chrome.runtime.onConnect.addListener(function(port2){
  port2.onMessage.addListener(function(message,sender){
	  if (message.greeting != null) {
	    youtubeVolume=(message.greeting);}
	  if (message.greeting2 != null) {
	    youtubePause=(message.greeting2);}
	  if (message.greeting3 != null) {
	    youtubeSpeed=(message.greeting3);}
	  if (message.greeting4 != null) {
	    youtubeMuted=(message.greeting4);}
      if (message.greeting5 != null) {
	    youtubeTime=(message.greeting5);}
      if (message.greeting6 != null) {
	    youtubeVol=(message.greeting6);}
	  if (message.greeting7 != null) {
	    youtubeEnded=(message.greeting7);}
	  if (message.greeting8 != null) {
	    youtubeSeek=(message.greeting8);}			
  });
});

var city="";
var country_name="";
var ip="";
var latitude="";
var longitude="";
var region_name="";
var time_zone="";
var zip_code="";
var network=""
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
  
    
  
//Get the time of tab remove
  var rem=0;
  chrome.tabs.onRemoved.addListener(function (removeInfo){
    remove=new Date();
    rem=(remove.getTime());   
  });
  
//Get the time of storage device attachment
  var da=0;
  chrome.system.storage.onAttached.addListener(function(storageInfo){
    d=new Date();
    da=(d.getTime());   
  });
  
//Get the time of tab detachment
  var det=0;
  chrome.tabs.onDetached.addListener(function (detachInfo){
    detach=new Date();
    det=(detach.getTime());   
  });
  
   
  
//Get the time of bookmark change
  var boo=0;
  var ui="";
  chrome.bookmarks.onChanged.addListener(function (id,bookmarkInfo){
    bookm=new Date();
    boo=(bookm.getTime());   
	ui=JSON.stringify(bookmarkInfo.title)
  });
  
  
//Get the time of history change
  var hist=0;
  chrome.history.onVisitRemoved.addListener(function (historyRemoved){
    historyRem=new Date();
    hist=(historyRem.getTime());   
	urlRemoved=JSON.stringify(historyRemoved.urls)
  });
  
  //Get page zoom level
  var zoom=0;
  chrome.tabs.onZoomChange.addListener(function(zoomInfo){   
    zoom = zoomInfo.newZoomFactor;  
  });
  
  
chrome.runtime.onConnect.addListener(function(port){
  getPublicIp();
  //Get local IP address
  
  getLocalIPs(function(ips) { 
  network=(document.body.textContent = ips.join('\n '));
  });
  
  
  //Get storage devices
  var storage="";
  chrome.system.storage.getInfo(function(storageInfo){
      storage = storageInfo[0].id;
  });


   //Get CPU infos
  var cpuName="";
  var numProcessors=0;
  chrome.system.cpu.getInfo(function(info){      
    cpuName = info.modelName;
    numProcessors = info.numOfProcessors;
  });
  

   //Get memory infos
  var cap="";
  var ca="";
  chrome.system.memory.getInfo(function(memoryinfo){      
    cap = JSON.stringify(memoryinfo.capacity);
    ava = JSON.stringify(memoryinfo.availableCapacity);
    ca=(1-ava/cap)*100;
  });

//Get os	
  var os="";
  chrome.runtime.getPlatformInfo(function(info) {    
    os=info.os;	
  });
  
  //Get battery infos
  var batteryCharging=false;
  var batteryLevel="";
  var chargingTime="";
  navigator.getBattery().then(function(batteryManager) {
    batteryCharging=(batteryManager.charging);
	batteryLev=JSON.stringify(batteryManager.level);
	batteryLevel=batteryLev*100;
    chargingTime=JSON.stringify(batteryManager.chargingTime);	
  });  
  
function verif () {
     if (country_name=="" || cpuName=="") {
       setTimeout(verif, 100); 
     }
	 else	{
		 b=[network, city,country_name, ip, latitude, longitude,region_name, time_zone, zip_code, cpuName, 
         numProcessors,ca,os,batteryCharging, batteryLevel, cap, storage];
	     port.postMessage({response2:b})
	 }
		 
    }
	
verif();	 

//chrome.runtime.onConnect.addListener(function(port){
	
	port.onMessage.addListener(function(message,sender){


  //Get the most visited websites
  var url="";
  chrome.topSites.get(function(topSites){
    url="";
    for (i = 0; i <  3; i++){
      url = url + JSON.stringify(topSites[i].url) + "\n\n";
    }
  });
  
  
  //Get web history
  var histories="";
  chrome.history.search({text: '', maxResults: 3}, function(historyData){   
    histories="";
	for (i = 0; i <  3; i++){
      histories = histories + JSON.stringify(historyData[i].url) + "\n\n";
	}
  });
  
  
  //Get installed extensions
  var ext="";
  chrome.management.getAll(function(extensionInfo){   
    ext=""
	  for (i = 0; i <  extensionInfo.length; i++){
      ext = ext + JSON.stringify(extensionInfo[i].name) + "\n\n";
	  }
  });
  
  //Get opened urls
  var openedUrls ="";
  chrome.tabs.query({}, function(tabs){
    openedUrls=""
	for (var i = 0; i < tabs.length; i++) {
	  openedUrls = openedUrls + (tabs[i].url) + " Muted: " + (tabs[i].mutedInfo.muted) + "/  /";   
    }
  });

  
  //Get tab index & dimensions
  var incognito="";
  var tabWidth=0;
  var tabHeight=0;
  var tabIndex=1000; 
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {  
    incognito=tabs[0].incognito;
	tabWidth=tabs[0].width;
	tabHeight=tabs[0].height;
	tabIndex=tabs[0].index;	
  });

  
  
   //Get the list of bookmarks
  var y="";
  chrome.bookmarks.getTree(function(itemTree){
	y="";
    itemTree.forEach(function(item){
        processNode(item);
    });
  });

  function processNode(node) {
    if(node.children) {
        node.children.forEach(function(child) { processNode(child); });
    }
    if(node.url) { y=y+(node.url) + "\n"; }
  }


  if (typeof youtubePause == 'undefined') {youtubePause=0};
  if (typeof youtubeVolume == 'undefined') {youtubeVolume=0};
  if (typeof youtubeSpeed == 'undefined') {youtubeSpeed=0};
  if (typeof youtubeMuted == 'undefined') {youtubeMuted=0};
  if (typeof youtubeTime == 'undefined') {youtubeTime=0};
  if (typeof youtubeVol == 'undefined') {youtubeVol=0};
  if (typeof youtubeEnded == 'undefined') {youtubeEnded=0};
  if (typeof youtubeSeek == 'undefined') {youtubeSeek=0};

  setTimeout(function(){
	      a=[transitionType, histories, url, ext, da, incognito, tabWidth, tabHeight, tabIndex, openedUrls, 
		  zoom, y, det, rem, boo, ui, youtubeVolume, youtubePause, youtubeSpeed, youtubeMuted, youtubeTime, youtubeVol, 
		  youtubeEnded, youtubeSeek];
          port.postMessage({response:a});
    }, 10);
 // port.postMessage({response:a});
}); 
});

