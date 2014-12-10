$(document).ready( function() {

    $('.results .box').hover( function() {
        $(this).css('background-color','#FAFAFA');
	$(this).css('border-color','#CCCCCC');
	$(this).css('cursor','pointer');
    }, function() {
	$(this).css('background-color','#FFFFFF');
	$(this).css('border-color','#DCDCDC');
	$(this).css('cursor','default');
    });

    $('.results .box').click( function() {
        var url = $(this).find('a').attr('href')
	window.location.href = url;
    });

});
