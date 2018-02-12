"use strict"

var bird_species = $("#default-blurb").html();
// console.log(bird_species);

$('#bird-pic').on('load', changePicture(bird_species));

function changePicture(species) {
    var bird_name = species.replace(/[.,\/#!$%\^&\*;:{}=\-_'~()]/g,"");
    var bird = bird_name.replace(/\s+/g, '-').toLowerCase();

    $.ajax({
        url: ("https://api.duckduckgo.com/?q="+bird+"&format=json&pretty=1&t=tellmeaboutthebirds"),
        jsonp: "callback",
        dataType: 'jsonp',
        xhrFields: { withCredentials: true},
        success: function(results){
            $("#picture-loader").hide();
            $("#picture-row").show();
            var image = results.Image;
            if (image == "") {
                image = "./static/images/bird_outline.png";
            }
            var abstract = results.Abstract;
            if (abstract == "") {
                abstract = "No information available.";
            }
            $("#bird-pic").attr("src", image);
            $("#abstract").html(abstract);
            
        }
    });
    
}