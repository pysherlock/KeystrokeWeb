var port2 = chrome.runtime.connect({name:"mycontentscript"});
var vid = $('video').get(0);

vid.addEventListener('volumechange', function(e) {
   d=new Date();
   da=(d.getTime());
   port2.postMessage({greeting:da});
   port2.postMessage({greeting6:vid.volume.toFixed(2)});
   if (vid.muted) {
	 port2.postMessage({greeting4:da});   
   }
});

vid.addEventListener('pause', function(e) {
   l=new Date();
   la=(l.getTime());
   port2.postMessage({greeting2:la});
});

vid.addEventListener('ratechange', function(e) {
   l=new Date();
   la=(l.getTime());
   port2.postMessage({greeting3:la});
});

//  display the current and remaining times
vid.addEventListener('timeupdate', function (e) {
  //  Current time  
  vTime = vid.currentTime;
  s = vTime.toFixed(1);
  port2.postMessage({greeting5:s});
});

vid.addEventListener('ended', function (e) {
   en=new Date();
   end=(en.getTime());
   port2.postMessage({greeting7:end});
});

vid.addEventListener('seeked', function (e) {
   se=new Date();
   see=(se.getTime());
   port2.postMessage({greeting8:see});
});

