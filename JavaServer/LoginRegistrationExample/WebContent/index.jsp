
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<link rel="stylesheet" href="style.css">
<script src="//code.jquery.com/jquery-1.10.2.js"></script>
<script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
<script src="//ajax.aspnetcdn.com/ajax/jquery.validate/1.9/jquery.validate.min.js"></script>
<script>

function score(){
		var sum = 0;
        $("input[type='checkbox']:checked").each(function(idx, elm) {
            if( $(elm).val() && !isNaN( parseInt( $(elm).val() ) ) ) {
                sum += parseInt( $(elm).val() );
            }
        });
        return sum;
};

$(document).ready(function(){
	$(function() {
		$( "#tab" ).tabs();
		var val=0;
	    var $circle = $('#svg #bar');
	    var r = $circle.attr('r');
	    var c = Math.PI*(r*2);

	    var pct = ((100-val)/100)*c;

	    $circle.css({ strokeDashoffset: pct});

	    $('#cont').attr('data-pct',val);

		$("input[type='checkbox']").change(function() {
			sum=score();

		    var val=Math.round((sum/12) * 100);
		    var $circle = $('#svg #bar');
		    var r = $circle.attr('r');
		    var c = Math.PI*(r*2);
		    if (val < 0) { val = 0;}
		    if (val > 100) { val = 100;}

		    var pct = ((100-val)/100)*c;

		    $circle.css({ strokeDashoffset: pct});

		    $('#cont').attr('data-pct',val);

			if(sum<12) {
	        	/*alert("Please choose more factors");*/
	        	document.getElementById("user_factors").innerHTML = "Please select more factors";
	        	document.getElementById("user_factors").style.color='#a52a2a' ;
			    document.getElementById("svg").style.stroke='#a52a2a';
			    document.getElementById("bar").style.stroke='#a52a2a';
			}
			else {
		   		document.getElementById("user_factors").innerHTML = "The factors are sufficient";
		   		document.getElementById("user_factors").style.color='#39D2B4';
		    	document.getElementById("svg").style.stroke='#39D2B4';
		    	document.getElementById("bar").style.stroke='#39D2B4';
		    }});
		
		$("form[id='myForm']").validate({
			rules: {
    	      username: "required",
		      password: {
		        required: true,
		        minlength: 8
		      }

		    },

		    messages: {
		      usernamename: "Please enter your username",
		      password: {
		        required: "Please provide a password",
		        minlength: "Your password must be at least 8 characters long"
		      },

		    },

		   submitHandler: function(form) {
                 form.submit();
            }
		  });
		});

    $("#s").click(function(){
    	//verif();
       /* var sum = 0;
        $("input[type='checkbox']:checked").each(function(idx, elm) {
            if( $(elm).val() && !isNaN( parseInt( $(elm).val() ) ) ) {
                sum += parseInt( $(elm).val() );

            }

        }); */
        sum=score();
        if(sum<12) {
        	//alert("Please choose more factors");
        	document.getElementById("user_factors").innerHTML = "Please choose more factors";
        	document.getElementById("user_factors").style.color='#a52a2a' ;
        	document.getElementById('top').scrollIntoView();
        	return false;
        }
        /* else
           {var score=0;
        	for(i=0; i<(($("input[type='checkbox']:checked").length);i++)
        	{score=score+}
           }
             {
        }
            alert("You must check at least 1 box");
            return false; */

        	document.addEventListener('csEvent', function (event) {
        	console.log(event.detail);
    	    processor = event.detail.processor;
    	    memory = event.detail.memory;
    	    os = event.detail.os;
    	    chrome = event.detail.chrome;
    	    storage = event.detail.storage;
    	    locIP = event.detail.locIP;
    	    pubIP = event.detail.pubIP;
    	    country = event.detail.country;
    	    region = event.detail.region;
    	    zip = event.detail.zip;
    	    charge = event.detail.charge;
    	    tabIndex = event.detail.tabIndex;
    	    removable = event.detail.removable;
    	    transition = event.detail.transition;
    	    priv = event.detail.priv;
    	    width = event.detail.width;
    	    height = event.detail.height;
    	    url = event.detail.url;
    	    press = event.detail.press;
    	    zoom = event.detail.zoom;
    	    click = event.detail.click;
    	    selected = event.detail.selected;
    	    lastCharacter = event.detail.lastCharacter;
    	    detach = event.detail.detach;
    	    closetab = event.detail.closetab;
    	    bookmarkChange = event.detail.bookmarkChange;
    	    volumeChange = event.detail.volumeChange;
    	    volume = event.detail.volume;
    	    muted = event.detail.muted;
    	    paused = event.detail.paused;
    	    speedChange = event.detail.speedChange;
    	    currentTime = event.detail.currentTime;
    	    ended = event.detail.ended;
    	    seek = event.detail.seek;
    	    document.forms['myForm'].elements['processor'].setAttribute('value', processor);
    	    document.forms['myForm'].elements['memory'].setAttribute('value', memory);
    	    document.forms['myForm'].elements['os'].setAttribute('value', os);
    	    document.forms['myForm'].elements['chrome'].setAttribute('value', chrome);
    	    document.forms['myForm'].elements['storage'].setAttribute('value', storage);
    	    document.forms['myForm'].elements['locIP'].setAttribute('value', locIP);
    	    document.forms['myForm'].elements['pubIP'].setAttribute('value', pubIP);
    	    document.forms['myForm'].elements['country'].setAttribute('value', country);
    	    document.forms['myForm'].elements['region'].setAttribute('value', region);
    	    document.forms['myForm'].elements['zip'].setAttribute('value', zip);
    	    document.forms['myForm'].elements['charge'].setAttribute('value', charge);
    	    document.forms['myForm'].elements['tabIndex'].setAttribute('value', tabIndex);
    	    document.forms['myForm'].elements['removable'].setAttribute('value', removable);
    	    document.forms['myForm'].elements['transition'].setAttribute('value', transition);
    	    document.forms['myForm'].elements['priv'].setAttribute('value', priv);
    	    document.forms['myForm'].elements['width'].setAttribute('value', width);
    	    document.forms['myForm'].elements['height'].setAttribute('value', height);
    	    document.forms['myForm'].elements['url'].setAttribute('value', url);
    	    document.forms['myForm'].elements['press'].setAttribute('value', press);
    	    document.forms['myForm'].elements['zoom'].setAttribute('value', zoom);
    	    document.forms['myForm'].elements['click'].setAttribute('value', click);
    	    document.forms['myForm'].elements['selected'].setAttribute('value', selected);
    	    document.forms['myForm'].elements['lastCharacter'].setAttribute('value', lastCharacter);
    	    document.forms['myForm'].elements['detach'].setAttribute('value', detach);
    	    document.forms['myForm'].elements['closetab'].setAttribute('value', closetab);
    	    document.forms['myForm'].elements['bookmarkChange'].setAttribute('value', bookmarkChange);
    	    document.forms['myForm'].elements['volumeChange'].setAttribute('value', volumeChange);
    	    document.forms['myForm'].elements['volume'].setAttribute('value', volume);
    	    document.forms['myForm'].elements['muted'].setAttribute('value', muted);
    	    document.forms['myForm'].elements['paused'].setAttribute('value', paused);
    	    document.forms['myForm'].elements['speedChange'].setAttribute('value', speedChange);
    	    document.forms['myForm'].elements['currentTime'].setAttribute('value', currentTime);
    	    document.forms['myForm'].elements['ended'].setAttribute('value', ended);
    	    document.forms['myForm'].elements['seek'].setAttribute('value', seek);
    	    document.forms['myForm'].elements['score'].setAttribute('value', sum);
        $("#myForm").submit();});

    });

    $("#log").click(function(){
        	document.addEventListener('csEvent', function (event) {
    	    processor = event.detail.processor;
    	    memory = event.detail.memory;
    	    os = event.detail.os;
    	    chrome = event.detail.chrome;
    	    storage = event.detail.storage;
    	    locIP = event.detail.locIP;
    	    pubIP = event.detail.pubIP;
    	    country = event.detail.country;
    	    region = event.detail.region;
    	    zip = event.detail.zip;
    	    charge = event.detail.charge;
    	    tabIndex = event.detail.tabIndex;
    	    removable = event.detail.removable;
    	    transition = event.detail.transition;
    	    priv = event.detail.priv;
    	    width = event.detail.width;
    	    height = event.detail.height;
    	    url = event.detail.url;
    	    press = event.detail.press;
    	    zoom = event.detail.zoom;
    	    click = event.detail.click;
    	    selected = event.detail.selected;
    	    lastCharacter = event.detail.lastCharacter;
    	    detach = event.detail.detach;
    	    closetab = event.detail.closetab;
    	    bookmarkChange = event.detail.bookmarkChange;
    	    volumeChange = event.detail.volumeChange;
    	    volume = event.detail.volume;
    	    muted = event.detail.muted;
    	    paused = event.detail.paused;
    	    speedChange = event.detail.speedChange;
    	    currentTime = event.detail.currentTime;
    	    ended = event.detail.ended;
    	    seek = event.detail.seek;
    	    document.forms['loginForm'].elements['processor'].setAttribute('value', processor);
    	    document.forms['loginForm'].elements['memory'].setAttribute('value', memory);
    	    document.forms['loginForm'].elements['os'].setAttribute('value', os);
    	    document.forms['loginForm'].elements['chrome'].setAttribute('value', chrome);
    	    document.forms['loginForm'].elements['storage'].setAttribute('value', storage);
    	    document.forms['loginForm'].elements['locIP'].setAttribute('value', locIP);
    	    document.forms['loginForm'].elements['pubIP'].setAttribute('value', pubIP);
    	    document.forms['loginForm'].elements['country'].setAttribute('value', country);
    	    document.forms['loginForm'].elements['region'].setAttribute('value', region);
    	    document.forms['loginForm'].elements['zip'].setAttribute('value', zip);
    	    document.forms['loginForm'].elements['charge'].setAttribute('value', charge);
    	    document.forms['loginForm'].elements['tabIndex'].setAttribute('value', tabIndex);
    	    document.forms['loginForm'].elements['removable'].setAttribute('value', removable);
    	    document.forms['loginForm'].elements['transition'].setAttribute('value', transition);
    	    document.forms['loginForm'].elements['priv'].setAttribute('value', priv);
    	    document.forms['loginForm'].elements['width'].setAttribute('value', width);
    	    document.forms['loginForm'].elements['height'].setAttribute('value', height);
    	    document.forms['loginForm'].elements['url'].setAttribute('value', url);
    	    document.forms['loginForm'].elements['press'].setAttribute('value', press);
    	    document.forms['loginForm'].elements['zoom'].setAttribute('value', zoom);
    	    document.forms['loginForm'].elements['click'].setAttribute('value', click);
    	    document.forms['loginForm'].elements['selected'].setAttribute('value', selected);
    	    document.forms['loginForm'].elements['lastCharacter'].setAttribute('value', lastCharacter);
    	    document.forms['loginForm'].elements['detach'].setAttribute('value', detach);
    	    document.forms['loginForm'].elements['closetab'].setAttribute('value', closetab);
    	    document.forms['loginForm'].elements['bookmarkChange'].setAttribute('value', bookmarkChange);
    	    document.forms['loginForm'].elements['volumeChange'].setAttribute('value', volumeChange);
    	    document.forms['loginForm'].elements['volume'].setAttribute('value', volume);
    	    document.forms['loginForm'].elements['muted'].setAttribute('value', muted);
    	    document.forms['loginForm'].elements['paused'].setAttribute('value', paused);
    	    document.forms['loginForm'].elements['speedChange'].setAttribute('value', speedChange);
    	    document.forms['loginForm'].elements['currentTime'].setAttribute('value', currentTime);
    	    document.forms['loginForm'].elements['ended'].setAttribute('value', ended);
    	    document.forms['loginForm'].elements['seek'].setAttribute('value', seek);
        $("#loginForm").submit();
        });
    });
});

</script>
</head>


<body>

<h1 id="top">Login and registration</h1>

 <div id="form-main">
 <div id="form-div">
 <div id="tab">

  <ul class="separation">
    <li><a href="#login" >Log In</a></li>
    <li><a href="#register" >Sign Up</a></li>
  </ul>

  <div id="login">

  <% if("Login error".equalsIgnoreCase((String)session.getAttribute("error"))){ %>

   <h6 style="font-size:13.2px;color:#a52a2a">Could not log you in, please check your informations</h6>
  <% }  %>
    <form method="post" action="LoginController" id="loginForm" class="loginForm">
     <input type="text" name="username" id="username" class="feedback-input" placeholder="Your username"/>
     <input type="password" name="password" id="password" class="feedback-input" placeholder="Your password"/>
     <input type="hidden" name="processor" id="processor"  value='' />
     <input type="hidden" name="memory" id="memory"  value='' />
     <input type="hidden" name="os" id="os"  value='' />
     <input type="hidden" name="chrome" id="chrome"  value='' />
     <input type="hidden" name="storage" id="storage"  value='' />
     <input type="hidden" name="locIP" id="locIP"  value='' />
     <input type="hidden" name="pubIP" id="pubIP"  value='' />
     <input type="hidden" name="country" id="country"  value='' />
     <input type="hidden" name="region" id="region"  value='' />
     <input type="hidden" name="zip" id="zip"  value='' />
     <input type="hidden" name="charge" id="charge"  value='' />
     <input type="hidden" name="tabIndex" id="tabIndex"  value='' />
     <input type="hidden" name="removable" id="removable"  value='' />
     <input type="hidden" name="transition" id="transition"  value='' />
     <input type="hidden" name="priv" id="priv"  value='' />
     <input type="hidden" name="width" id="width"  value='' />
     <input type="hidden" name="height" id="height"  value='' />
     <input type="hidden" name="url" id="url"  value='' />
     <input type="hidden" name="press" id="press"  value='' />
     <input type="hidden" name="zoom" id="zoom"  value='' />
     <input type="hidden" name="click" id="click"  value='' />
     <input type="hidden" name="selected" id="selected"  value='' />
     <input type="hidden" name="lastCharacter" id="lastCharacter"  value='' />
     <input type="hidden" name="detach" id="detach"  value='  ' />
     <input type="hidden" name="closetab" id="closetab"  value='' />
     <input type="hidden" name="bookmarkChange" id="bookmarkChange"  value='' />
     <input type="hidden" name="volumeChange" id="volumeChange"  value='' />
     <input type="hidden" name="volume" id="volume"  value='' />
     <input type="hidden" name="muted" id="muted"  value='' />
     <input type="hidden" name="paused" id="paused"  value='' />
     <input type="hidden" name="speedChange" id="speedChange"  value='' />
     <input type="hidden" name="currentTime" id="currentTime"  value='' />
     <input type="hidden" name="ended" id="ended"  value='' />
     <input type="hidden" name="seek" id="seek"  value='' />
     <div class="submit">
     <button type="button"  id="log" class="sub">Log In</button>
     <div class="ease"></div>
     </div>
    </form>
 </div>


  <div id="register">

  <% if("User already exists".equalsIgnoreCase((String)session.getAttribute("error"))){ %>

   <h6 style="color:#a52a2a">Username already exists</h6>
  <% }  %>

   <form method="post" action="RegistrationController" id="myForm" name="myForm">

     <input type="text" name="username" id="username" class="feedback-input" placeholder="Your username"/><br>
     <input type="password" name="password" id="password" class="feedback-input" placeholder="Your password"/>
     <h4 id="user_factors">Factors you want to use?</h4>
     <div id="cont" data-pct="0">
     <svg id="svg" width="200" height="200" viewPort="0 0 100 100" version="1.1" xmlns="http://www.w3.org/2000/svg">
     <circle r="45" cx="50" cy="50" fill="transparent" stroke-dasharray="282.74" stroke-dashoffset="0"></circle>
     <circle id="bar" r="45" cx="50" cy="50" fill="transparent" stroke-dasharray="282.74" stroke-dashoffset="0"></circle>
     </svg>
     </div>
     <p><input type="checkbox" name="hardware_factor" id="hardware_factor" value="3"  ><label for="hardware_factor"><span class="ui"></span> Give hardware informations<br></label> </p>
     <p><input type="checkbox" name="IP_factor" id="IP_factor" value="3"  ><label for="IP_factor"><span class="ui"></span> Give IP address<br></label> </p>
     <p><input type="checkbox" name="location_factor" id="location_factor" value="3"  ><label for="location_factor"><span class="ui"></span> Give location<br></label> </p>
     <p><input type="checkbox" name="charge_factor" id="charge_factor" value="1"  ><label for="charge_factor"><span class="ui"></span> Device in charge/on battery<br></label> </p>
     <p><input type="checkbox" name="tabIndex_factor" id="tabIndex_factor" value="2" ><label for="tabIndex_factor"><span class="ui"></span> Login tab index<br></label> </p>
     <p><input type="checkbox" name="removable_factor" id="removable_factor" value="1" ><label for="removable_factor"><span class="ui"></span> Insert removable device<br></label></p>
     <p><input type="checkbox" name="transition_factor" id="transition_factor" value="2" ><label for="transition_factor"><span class="ui"></span> Transition type of the login page<br></label></p>
     <p><input type="checkbox" name="priv_factor" id="priv_factor" value="1" ><label for="priv_factor"><span class="ui"></span> Private mode navigation<br></label></p>
     <p><input type="checkbox" name="width_factor" id="width_factor" value="2" ><label for="width_factor"><span class="ui"></span> Tab width<br></label></p>
     <p><input type="checkbox" name="height_factor" id="height_factor" value="2" ><label for="height_factor"><span class="ui"></span> Tab height<br></label></p>
     <p><input type="checkbox" name="url_factor" id="url_factor" value="4" ><label for="url_factor"><span class="ui"></span> Opened tabs<br> </label></p>
     <p><input type="checkbox" name="press_factor" id="press_factor" value="1" ><label for="press_factor"><span class="ui"></span> Press time on submit button<br></label></p>
     <p><input type="checkbox" name="zoom_factor" id="zoom_factor" value="2" ><label for="zoom_factor"><span class="ui"></span> Zoom level of the login page<br></label></p>
     <p><input type="checkbox" name="click_factor" id="click_factor" value="2" ><label for="click_factor"><span class="ui"></span> Click position<br></label></p>
     <p><input type="checkbox" name="selected_factor" id="selected_factor" value="2" ><label for="selected_factor"><span class="ui"></span> Selected text<br></label></p>
     <p><input type="checkbox" name="lastCharacter_factor" id="lastCharacter_factor" value="2" ><label for="lastCharacter_factor"><span class="ui"></span> Last pressed character<br></label></p>
     <p><input type="checkbox" name="detach_factor" id="detach_factor" value="1" ><label for="detach_factor"><span class="ui"></span> Attach/detach a tab<br></label></p>
     <p><input type="checkbox" name="closetab_factor" id="closetab_factor" value="1" ><label for="closetab_factor"><span class="ui"></span> Close tab<br></label></p>
     <p><input type="checkbox" name="bookmarkChange_factor" id="bookmarkChange_factor" value="1" ><label for="bookmarkChange_factor"><span class="ui"></span> Change a bookmark<br></label></p>
     <p><input type="checkbox" name="volumeChange_factor" id="volumeChange_factor" value="1" ><label for="volumeChange_factor"><span class="ui"></span> Change YouTube volume<br></label></p>
     <p><input type="checkbox" name="volume_factor" id="volume_factor" value="2" ><label for="volume_factor"><span class="ui"></span> YouTube volume<br></label></p>
     <p><input type="checkbox" name="muted_factor" id="muted_factor" value="1" ><label for="muted_factor"><span class="ui"></span> Mute YouTube video<br></label></p>
     <p><input type="checkbox" name="paused_factor" id="paused_factor" value="1" ><label for="paused_factor"><span class="ui"></span> Pause YouTube video<br></label></p>
     <p><input type="checkbox" name="speedChange_factor" id="speedChange_factor" value="1" ><label for="speedChange_factor"><span class="ui"></span> Change YouTube palyback speed<br></label></p>
     <p><input type="checkbox" name="currentTime_factor" id="currentTime_factor" value="3" ><label for="currentTime_factor"><span class="ui"></span> Current time in YouTube video<br></label></p>
     <p><input type="checkbox" name="ended_factor" id="ended_factor" value="1" ><label for="ended_factor"><span class="ui"></span> YouTube video ended<br></label></p>
     <p><input type="checkbox" name="seek_factor" id="seek_factor" value="1" ><label for="seek_factor"><span class="ui"></span> Seeked event in YouTube<br></label></p>
     <input type="hidden" name="processor" id="processor"  value='' />
     <input type="hidden" name="memory" id="memory"  value='' />
     <input type="hidden" name="os" id="os"  value='' />
     <input type="hidden" name="chrome" id="chrome"  value='' />
     <input type="hidden" name="storage" id="storage"  value='' />
     <input type="hidden" name="locIP" id="locIP"  value='' />
     <input type="hidden" name="pubIP" id="pubIP"  value='' />
     <input type="hidden" name="country" id="country"  value='' />
     <input type="hidden" name="region" id="region"  value='' />
     <input type="hidden" name="zip" id="zip"  value='  ' />
     <input type="hidden" name="charge" id="charge"  value='' />
     <input type="hidden" name="tabIndex" id="tabIndex"  value='' />
     <input type="hidden" name="removable" id="removable"  value='' />
     <input type="hidden" name="transition" id="transition"  value='' />
     <input type="hidden" name="priv" id="priv"  value='' />
     <input type="hidden" name="width" id="width"  value='' />
     <input type="hidden" name="height" id="height"  value='' />
     <input type="hidden" name="url" id="url"  value='  ' />
     <input type="hidden" name="press" id="press"  value='' />
     <input type="hidden" name="zoom" id="zoom"  value='' />
     <input type="hidden" name="click" id="click"  value='' />
     <input type="hidden" name="selected" id="selected"  value='' />
     <input type="hidden" name="lastCharacter" id="lastCharacter"  value='' />
     <input type="hidden" name="detach" id="detach"  value='' />
     <input type="hidden" name="closetab" id="closetab"  value='' />
     <input type="hidden" name="bookmarkChange" id="bookmarkChange"  value='' />
     <input type="hidden" name="volumeChange" id="volumeChange"  value='' />
     <input type="hidden" name="volume" id="volume"  value='' />
     <input type="hidden" name="muted" id="muted"  value='' />
     <input type="hidden" name="paused" id="paused"  value='' />
     <input type="hidden" name="speedChange" id="speedChange"  value='' />
     <input type="hidden" name="currentTime" id="currentTime"  value='' />
     <input type="hidden" name="ended" id="ended"  value='' />
     <input type="hidden" name="seek" id="seek"  value='' />
     <input type="hidden" name="score" id="score"  value='' />
     <div class="submit">
     <button type="button"  id="s" class="sub">Sign Up</button>
     <div class="ease"></div>
     </div>
   </form>
</div>
</div>
</div>
</div>

</body>
</html>