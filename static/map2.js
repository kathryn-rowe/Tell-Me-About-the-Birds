"use strict"
var D;
var d;
function renderMap(api_key, longitude, latitude, birding_data){

    D = birding_data;
    mapboxgl.accessToken = api_key;

    var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/streets-v9', //stylesheet location
        center: [longitude, latitude], // starting position
        // center: [-121.403732, 40.492392],
        zoom: 9 // starting zoom
    });
    // map.scrollZoom.disable();
    
    var months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ];

    function updateMap(bird_data) {

        d = bird_data;
        var map1 = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/streets-v9', //stylesheet location
        center: [longitude, latitude], // starting position
        // center: [-121.403732, 40.492392],
        zoom: 9 // starting zoom
        });
    // //     // console.log(data.features)
    //     map.eachLayer(function (layer) {
    //         map.removeLayer(layer);
    //     });
    // bird_data = bird_data.features[0];
     map1.on('load', function(bird_data){
        console.log(bird_data);
        bird_data = d;
        debugger;
        map1.addSource("birding-locations", {
            "type": "geojson",
            "data": bird_data,
            "buffer": 25,
            "cluster": true,
            "clusterMaxZoom": 19,
            "clusterRadius": 20,
        });

        var layers = [
            [0, 'green'],
            [20, 'orange'],
            [200, 'red']
        ];

        layers.forEach(function (layer, i) {
            map1.addLayer({
                "id": "bird_count" + i,
                "type": "circle",
                "source": "birding-locations",
                "paint": {
                    "circle-color": layer[1],
                    "circle-radius": 20,
                    // "circle-blur": 1
                },
            "filter": i === layers.length - 1 ?
                [">=", "point_count", layer[0]] :
                ["all",
                    [">=", "point_count", layer[0]],
                    ["<", "point_count", layers[i + 1][0]]]
            });
        });
        map1.addLayer({
            "id": "unclustered-points",
            "type": "circle",
            "source": "birding-locations",
            "paint": {
                "circle-color": 'black',
                "circle-radius": 5,
                "circle-blur": 1
            },
            "filter": ["!has", "point_count"]
        });
        map1.addLayer({
            "id": "cluster-count",
            "type": "symbol",
            "source": "birding-locations",
            "layout": {
                "text-field": "{point_count}",
                "text-font": [
                    "DIN Offc Pro Medium",
                    "Arial Unicode MS Bold"
                ],
                "text-size": 12
            }
        });
            
        // filterBy(0);
        // //Connect slider with map; gets the current month as an integer
        // document.getElementById('slider').addEventListener('input', function(evt) {
        //     var month = parseInt(evt.target.value);
        //     filterBy(month);
        // });
    });
    }
    var data_per_month;

    function filterBy(evt) {
        // var filters = ['==', 'month', months[month]];
        // map.setFilter('bird_count0', filters);
        // map.setFilter('bird_count1', filters);
        // map.setFilter('bird_count2', filters);
        // map.setFilter('unclustered-points', filters);

        // Set the label to the month
        var month = parseInt(evt.target.value);
        document.getElementById('month').textContent = months[month];
        console.log(month);
        var data = birding_data['features']
        
        var desiredMonthData = []

        for (var i=0; i < data.length; i++) {
            if (data[i]['properties']['month'] === months[month]) {
                desiredMonthData.push(data[i]);
            }
        }
        // console.log(desiredMonthData);
        // function setMonthData(birdData) {
        //     data_per_month = birdData
        // }

        $.ajax({
            url: '/filter_geojson', 
            type: 'POST',
            contentType: 'application/json; charset=uft-8',
            data: JSON.stringify({'data': desiredMonthData}), 
            success: function(results) {
                var birdDataMonth = results.birdDataMonth;
                // debugger;
                console.log(birdDataMonth);
                updateMap(birdDataMonth);
                // setMonthData(birdDataMonth);
            }
        });
        // console.log(data_per_month);
    }

    // function setMonthData(birdData) {
    //         data_per_month = birdData;
    //         console.log(data_per_month);
    // }
    document.getElementById('slider').addEventListener("change", filterBy);

    // //Wait until the map loads before adding layers
    map.on('load', function () {
    //     // console.log(data.features)
        map.addSource("birding-locations", {
            "type": "geojson",
            "data": birding_data,
            "buffer": 25,
            "cluster": true,
            "clusterMaxZoom": 19,
            "clusterRadius": 20,
        });

        var layers = [
            [0, 'green'],
            [20, 'orange'],
            [200, 'red']
        ];

        layers.forEach(function (layer, i) {
            map.addLayer({
                "id": "bird_count" + i,
                "type": "circle",
                "source": "birding-locations",
                "paint": {
                    "circle-color": layer[1],
                    "circle-radius": 20,
                    // "circle-blur": 1
                },
            "filter": i === layers.length - 1 ?
                [">=", "point_count", layer[0]] :
                ["all",
                    [">=", "point_count", layer[0]],
                    ["<", "point_count", layers[i + 1][0]]]
            });
        });
        map.addLayer({
            "id": "unclustered-points",
            "type": "circle",
            "source": "birding-locations",
            "paint": {
                "circle-color": 'black',
                "circle-radius": 5,
                "circle-blur": 1
            },
            "filter": ["!has", "point_count"]
        });
        map.addLayer({
            "id": "cluster-count",
            "type": "symbol",
            "source": "birding-locations",
            "layout": {
                "text-field": "{point_count}",
                "text-font": [
                    "DIN Offc Pro Medium",
                    "Arial Unicode MS Bold"
                ],
                "text-size": 12
            }
        });
            
    }); 
}
function getData() {
    $.get("/get_data.json", function(results) {
        var api_key = results.mapbox_api_key;
        var latitude = results.latitude;
        var longitude = results.longitude;
        var birding_data = results.birding_locations;
        renderMap(api_key, longitude, latitude, birding_data);
    });
};

getData();