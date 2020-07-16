$('#registerEmail').on('input', function(){
	var re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	var is_email=re.test($('#registerEmail').val());
	$('#registerEmail').removeClass('is-invalid');
	if(($('#registerEmail').val().length > 7) && (is_email)){
		$('#registerEmail').removeClass('is-invalid').addClass('is-valid')
		$('#msg').html('');
	}else{
		$('#registerEmail').removeClass('is-valid').addClass('is-invalid');
		$('#msg').html('Enter a valid email address!');
	}
});

$('#aPass').on('input', function(){
	if(!(($('#aPass').val().length > 7) && (/\d/.test($('#aPass').val())))){
		$('#aPass').removeClass('is-valid').addClass('is-invalid');
		$('#msg2').html('Password minimum 8 characters with numeric values');
	}
	else{
		$('#msg2').html('');
		$('#aPass').removeClass('is-invalid').addClass('is-valid')
	}
});

$('#aPass2').on('input', function(){
	if($('#aPass').val() != $('#aPass2').val()){
		$('#aPass2').removeClass('is-valid').addClass('is-invalid');
		$('#msg2').html('Password didn\'t Match!');
	}else{
		$('#msg2').html('');
		$('#aPass2').removeClass('is-invalid').addClass('is-valid');
	}
});

$("#sign-up").click(function(event){
	var form_data=["#registerEmail", "#aPass", "#aPass2"];
	var error_free=true;
	for (var index in form_data){
		var element=$(form_data[index]);
		var isnotvalid=element.hasClass("is-invalid");
		var element_value=element.val()
		if (isnotvalid || !element_value){error_free=false;}
	}
	//var agree_check=$("#agreePolicy").is(":checked")
	//if(!agree_check){error_free=false}
	if (!error_free){
		event.preventDefault(); 
	}
});

$('#aPass, #aPass2').keypress(function(e) { 
	var s = String.fromCharCode( e.which );

	if((s.toUpperCase() === s && s.toLowerCase() !== s && !e.shiftKey) ||
	   (s.toUpperCase() !== s && s.toLowerCase() === s && e.shiftKey)){
		$('#capsWarning').html('Capslock is ON!');
	} else {
		$('#capsWarning').html('');
	}
});