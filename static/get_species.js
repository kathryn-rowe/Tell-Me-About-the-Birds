"use strict"

function getBirdSpecies(evt) {
    evt.preventDefault();
    
    var data = {"county": $('#location').val()}
    console.log(data);

    $.ajax({
        url: '/get_species.json',
        dataType: 'json',
        type: 'GET',
        data: data,
        success: function(data) {
            
            var len = data.length;

            $('#bird-species').empty();
            
            for ( var i = 0; i<len; i++) {
                $('#bird-species').append("<option value='"+data+"'>"+data+"</option>");
            }
        }
    });
}

$('#location').on('change', getBirdSpecies)