var t = 121; 

var x = setInterval(function() { 
    t = t-1;
    var seconds = t%60;
    var minutes = (t-seconds)/60; 
    if(minutes<10){minutes = "0"+minutes}
    if(seconds<10){seconds="0"+seconds}
    document.getElementById("timer").innerHTML = minutes + ":" + seconds; 
    if (t < 0) { 
        clearInterval(x); 
        document.getElementById("timer").innerHTML = ""; 
    } 
}, 1000); 

function sendverify(event){
    if(t>0){event.preventDefault()}
}