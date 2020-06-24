function show(){
    document.getElementById('new-colabs-form').setAttribute("class", "posting");
    document.getElementById('new').setAttribute("class", "hide register-new");
    document.getElementById('hide').setAttribute("class", "register-new");
}

function hide(){
    document.getElementById('new-colabs-form').setAttribute("class", "hide posting");
    document.getElementById('hide').setAttribute("class", "hide register-new");
    document.getElementById('new').setAttribute("class", "register-new");
}

