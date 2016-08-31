

var UI = function() {
	$('.button').mouseenter(function(){
		$('div').fadeTo('fast', 1);
	});

	$('.button').mouseleave(function(){
		$('div').fadeTo('fast', 0.5);
	});
};

$(document).ready(UI);