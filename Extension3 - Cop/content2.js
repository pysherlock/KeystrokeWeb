var port2 = chrome.runtime.connect({name:"mycontentscript"});
load();	  
function load() { 
  var vid = $('video').get(2);
  if (typeof vid == 'undefined') {
    window.requestAnimationFrame(load);
  }else {
  vid.addEventListener('volumechange', function(e) {
    d=new Date();
    volume_time=(d.getTime());
    port2.postMessage({greeting:volume_time});
    port2.postMessage({greeting6:vid.volume.toFixed(2)});
    if (vid.muted) {
    port2.postMessage({greeting4:volume_time});   
    }
  });

  vid.addEventListener('pause', function(e) {
    pa=new Date();
    pause=(pa.getTime());
    port2.postMessage({greeting2:pause});
  });

  vid.addEventListener('ratechange', function(e) {
    re=new Date();
    speed=(re.getTime());
    port2.postMessage({greeting3:speed});
  });

  vid.addEventListener('timeupdate', function (e) {
    vTime = vid.currentTime;
    current_time = vTime.toFixed(1);
    port2.postMessage({greeting5:current_time});
  });

  vid.addEventListener('ended', function (e) {
    en=new Date();
    end=(en.getTime());
    port2.postMessage({greeting7:end});
  });

  vid.addEventListener('seeked', function (e) {
    se=new Date();
    seek=(se.getTime());
    port2.postMessage({greeting8:seek});
  });
}}
