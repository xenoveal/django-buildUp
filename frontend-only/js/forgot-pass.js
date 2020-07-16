$('#registerEmail').on('input', function(){
	var re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	var is_email=re.test($('#registerEmail').val());

	if(($('#registerEmail').val().length > 7) && (is_email)){
		$('#registerEmail').removeClass('is-invalid').addClass('is-valid')
		$('#msg').html('');
	}else{
		$('#registerEmail').removeClass('is-valid').addClass('is-invalid');
		$('#msg').html('Enter a valid email address!');
	}
});

$("#forgot").click(function(event){
	var form_data=["#registerEmail"]
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