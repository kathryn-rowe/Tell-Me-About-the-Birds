"use strict"

function getBirdSpecies(evt) {
    evt.preventDefault();

    $.ajax({
        url: '/get_species.json',
        dataType: 'json',
        type: 'GET',
        data: {"county": $('#location').val()},
        success: function(data) {
            var len = data.length;

            $('#bird-species').empty();
            
            for ( var i = 0; i<len; i++) {
                $('#bird-species').append("<option value='"+data+"'>"+data[i]+"</option>");
            }
        }
    });
}

$('#location').on('change', getBirdSpecies);

// function showBirdSpecies(evt) {
//     $.ajax({
//         url: '/show_species',

//     })
$('#bird-species').on('change', function() {
    var bird = $('#bird-species option:selected').text();
    // console.log(bird);

    $.ajax({
        url: '/show_species',
        dataType: 'json',
        type: 'GET',
        data: {"bird": $('#bird-species option:selected').text()},
        success: function(data) {
            console.log(data);
        }
    })
});