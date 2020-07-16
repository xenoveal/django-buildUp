$(".top .profile img").click(function(){
    var x = $(".profile-expand")
    if(x.hasClass("hide")){
        x.removeClass("hide")
    }else{
        x.addClass("hide")
    }
})