"use strict"

var bird_species = $("#default-blurb").html();
// console.log(bird_species);

$('#bird-pic').on('load', changePicture(bird_species));

function changePicture(species) {
    var bird_name = species.replace(/[.,\/#!$%\^&\*;:{}=\-_'~()]/g,"");
    var bird = bird_name.replace(/\s+/g, '-').toLowerCase();

    $.ajax({
        url: ("http://api.duckduckgo.com/?q="+bird+"&format=json&pretty=1"),
        jsonp: "callback",
        dataType: 'jsonp',
        xhrFields: { withCredentials: true},
        success: function(results){
            $("#picture-loader").hide();
            $("#picture-row").show();
            var image = results.Image;
            if (image == "") {
                image = "./static/images/generic_bird.jpg";
            }
            var abstract = results.Abstract;
            $("#bird-pic").attr("src", image);
            $("#abstract").html(abstract);
            
        }
    });
    
}