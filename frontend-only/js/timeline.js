function pin(theid){
    var x = $("#"+theid)
    if(x.hasClass("active2")){
        x.removeClass("active2")
    }else{
        x.addClass("active2")
    }
}
function like(theid){
    var x = $("#"+theid)
    if(x.hasClass("active")){
        x.removeClass("active")
    }else{
        x.addClass("active")
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