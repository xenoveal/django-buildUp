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

$("#change").click(function(event){
	var form_data=["#aPass", "#aPass2"];
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
