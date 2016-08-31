

var UI = function() {
	$('.click').mouseenter(function(){
		$(this).fadeTo('fast', 1);
	});

	$('.click').mouseleave(function(){
		$(this).fadeTo('fast', 0.5);
	});
};



$(document).ready(UI);