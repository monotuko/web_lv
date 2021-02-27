
$(document).ready(function() {
	$('#errorAlert').hide();
	$('#successAlert').hide();
	$('form').on('submit', function(event) {
		var form_data = new FormData();
		form_data.append('text_file', $('#text_file')[0].files[0]);


		$.ajax({
			data: form_data,
			type : 'POST',
			url : '/process',
			processData: false,
   			contentType: false,
			async: false,
      		cache: false,
			error   : console.log('error'),
            success : console.log('success'),
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.filename).show();
				// $('#successData').text(JSON.stringify(data.content)).show();
				$('#errorAlert').hide();
			}
		});
		event.preventDefault();
	});
});