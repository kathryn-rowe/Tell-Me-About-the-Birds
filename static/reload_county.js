"use strict"

function reloadBirdSpecies(evt) {
    evt.preventDefault();

    $.ajax({
        url: '/get_species.json',
        dataType: 'json',
        type: 'GET',
        data: {"county": $('#new-county').val()},
        success: function(data) {
            var len = data.length;

            $('#bird-list').empty();
            
            for ( var i = 0; i<len; i++) {
                $('#bird-list').append("<option value='"+data+"'>"+data[i]+"</option>");
            }
        }
    });
}

$('#new-county').on('change', reloadBirdSpecies);

$('#submit-reload').on('click', function(evt){
    evt.preventDefault();
    console.log('hello');
    var countyName = $('#new-county').val();
    console.log(countyName);
    var birdName = $('#bird-list option:selected').text();
    console.log(birdName);
    

    $.ajax({
        url: "/reload_county.json",
        dataType: 'json',
        type: 'GET',
        data: {"bird": birdName, "county": countyName},
        success: function(results) {
            var api_key = results.mapbox_api_key;
            var latitude = results.latitude;
            var longitude = results.longitude;
            var birding_data = results.birding_locations;
            var bird_name = results.bird;
            var county_name = results.county;
            var zoomLevel = results.zoomLevel;
            changePicture(bird_name);
            renderMap(api_key, longitude, latitude, birding_data, zoomLevel);
            $('.map-overlay-inner').empty();
            $('.map-overlay-inner').html("<h2>"+bird_name + " Observations in " + county_name + " County, 2015</h2><label for='slider' id='month'>January</label><input id='slider' type='range' min='0' max='11' step='1' value='0' />");
        }
    });
});
// $('#bird-list').on('change', function() {
//     var bird = $('#bird-list option:selected').text();
//     // console.log(bird);

//     $.ajax({
//         url: '/show_species',
//         dataType: 'json',
//         type: 'GET',
//         data: {"bird": $('#bird-list option:selected').text()},
//         success: function(data) {
//             console.log(data);
//         }
//     })
// });