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
function like(theid){
    var x = $("#"+theid)
    if(x.hasClass("active")){
        x.removeClass("active")
        x.html(`<span class="iconify" data-icon="clarity:heart-line" data-inline="false"></span>`)
    }else{
        x.addClass("active")
        x.html(`<span class="iconify" data-icon="clarity:heart-solid" data-inline="false"></span>`)
    }
}
function comment(theid){
    var x = $("#"+theid)
    if(x.hasClass("hide")){
        x.removeClass("hide")
    }else{
        x.addClass("hide")
    }
}
$(".top .profile img").click(function(){
    var x = $(".profile-expand")
    if(x.hasClass("hide")){
        x.removeClass("hide")
    }else{
        x.addClass("hide")
    }
})
$("#filter").click(function(){
    var x = $("#filter-expand")
    if(x.hasClass("hide")){
        x.removeClass("hide")
    }else{
        x.addClass("hide")
    }
})