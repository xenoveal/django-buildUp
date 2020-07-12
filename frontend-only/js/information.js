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

$("#filter").click(function(){
    var x = $("#filter-expand")
    if(x.hasClass("hide")){
        x.removeClass("hide")
    }else{
        x.addClass("hide")
    }
})