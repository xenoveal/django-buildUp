
function toggle_show(theid) {
    var x = document.getElementById(theid);
	var showlogo = $('#'+theid+'show');
	var hidelogo = $('#'+theid+'hide');
    if (x.type === "password") {
        x.type = "text";
        hidelogo.css("display", "block")
        showlogo.css("display", "none")
    } else {
        x.type = "password";
        showlogo.css("display", "block")
        hidelogo.css("display", "none")
    }
} 