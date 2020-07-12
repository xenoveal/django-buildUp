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

function comment(theid){
    var x = $("#"+theid)
    if(x.hasClass("hide")){
        x.removeClass("hide")
    }else{
        x.addClass("hide")
    }
}

function pin(theid){
    var x = $("#"+theid)
    if(x.hasClass("active2")){
        x.removeClass("active2")
        x.html(`<span class="iconify" data-icon="bi:bookmark" data-inline="false"></span>`)
    }else{
        x.addClass("active2")
        x.html(`<span class="iconify" data-icon="bi:bookmark-fill" data-inline="false"></span>`)
    }
}