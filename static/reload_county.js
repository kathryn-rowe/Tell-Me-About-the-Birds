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
    // console.log('hello');
    var countyName = $('#new-county').val();
    console.log(countyName);
    var birdName = $('#bird-list option:selected').text();
    console.log(birdName);
    $("#map-loader").show();
    

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
            // this change
            $("#map-loader").hide();
            $('.map-overlay-inner').empty();
            $('.map-overlay-inner').html("<h2>"+bird_name + " Observations in " + county_name + " County, 2015</h2><label for='slider' id='month'>January</label><input id='slider' type='range' min='0' max='11' step='1' value='0' /><div><div id='bird-legend' class='legend'><div class='leg-circle'><span id'style_5' style='background-color: #f29e00'></span>80+</div><div class='leg-circle'><span id'style_4' style='background-color: #f29e00'></span>60 - 79</div><div class='leg-circle'><span id'style_3' style='background-color: #f29e00'></span>41 - 60</div><div class='leg-circle'><span id'style_2' style='background-color: #f29e00'></span>21 - 40</div><div class='leg-circle'><span id'style_1' style='background-color: #f29e00'></span>0 - 20</div></div></div>");
        }
    });
});
