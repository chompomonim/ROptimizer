$(function() {

    $(':radio').click(function () {
	var dataString = 'period=' + $(this).val();
	$.ajax({
	    type: "POST",
	    url: "/active_period",
	    data: dataString,
	    success: function() {

	    }
	});
    });

    $('#show-incomes').click(function() {
	if ($('#incomes').css('display') === 'none') {
	    $('#incomes').show();
	}
	else {
	    $('#incomes').hide();
	}
    });

    $('#show-expenses').click(function() {
	if ($('#expenses').css('display') === 'none') {
	    $('#expenses').show();
	}
	else {
	    $('#expenses').hide();
	}
    });

    $('#show-periods').click(function() {
	if ($('#periods').css('display') === 'none') {
	    $('#periods').show();
	}
	else {
	    $('#periods').hide();
	}
    });

});
