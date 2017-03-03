"use strict"

function changePicture(species) {
    var bird_name = species.replace(/[.,\/#!$%\^&\*;:{}=\-_'~()]/g,"");
    var bird = bird_name.replace(/\s+/g, '-').toLowerCase();
    console.log("I'm here");
    $.ajax({
        url: ("http://api.duckduckgo.com/?q="+bird+"&format=json&pretty=1"),
        jsonp: "callback",
        dataType: 'jsonp',
        xhrFields: { withCredentials: true},
        success: function(results){
            var image = results.Image;
            var abstract = results.Abstract;
            $("#birdz-rule").attr("src", image);
            $("#abstract").html(abstract);
        }
    });
    
}