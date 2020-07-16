$('#loginEmail').on('input', function(){
	var re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	var is_email=re.test($('#loginEmail').val());

	if(($('#loginEmail').val().length > 7) && (is_email)){
		$('#loginEmail').removeClass('is-invalid').addClass('is-valid')
		$('#msg').html('');
	}else{
		$('#loginEmail').removeClass('is-valid').addClass('is-invalid');
		$('#msg').html('Enter a valid email address!');
	}
});

$('#aPass').keypress(function(e) { 
	var s = String.fromCharCode( e.which );

	if((s.toUpperCase() === s && s.toLowerCase() !== s && !e.shiftKey) ||
	   (s.toUpperCase() !== s && s.toLowerCase() === s && e.shiftKey)){
		$('#capsWarning').html('Capslock is ON!');
	} else {
		$('#capsWarning').html('');
	}
});

$("#sign-in").click(function(event){
	var form_data=["#loginEmail", "#aPass"]
	var error_free=true;
	for (var index in form_data){
		var element=$(form_data[index]);
		var isnotvalid=element.hasClass("is-invalid");
		var element_value=element.val()
		if (isnotvalid || !element_value){error_free=false;}
	}
	if (!error_free){
		event.preventDefault(); 
	}
});