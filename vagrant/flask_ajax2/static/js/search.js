$(document).ready(function() {
	$('#drop-name').on('click', function() {
		$('#user-column').val('Name');
	});
	$('#drop-lat-name').on('click', function() {
		$('#user-column').val('Latin Name');
	});
	$('#drop-type').on('click', function() {
		$('#user-column').val('Type');
	});
	$('#drop-edible').on('click', function() {
		$('#user-column').val('Edible');
		$('#user-input').val('Yes');
	});
	$('#drop-poisonous').on('click', function() {
		$('#user-column').val('Poisonous');
		$('#user-input').val('Yes');
	});
});

$(document).ready(function() {

	$(document).bind('click', '#search-btn', function(event) {

		req=$.ajax({
			data : {
				column: $('input[name="column"]').val(),
				input: $('input[name="input"]').val()
			},
			type: 'POST',
			url: '/search_results'

		});
		req.done(function(data) {
			$('#results').html(data);
		})

		event.preventDefault();

	});

});