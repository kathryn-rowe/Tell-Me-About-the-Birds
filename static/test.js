"use strict"

function showAlert(){
    $.get("/get_api_key", function(results) {
        console.log("inside hello");
        console.log(results);
    });
}

$('#slider').on('click', showAlert);
