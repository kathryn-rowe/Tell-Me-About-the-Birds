"use strict"

var map;

function renderMap(api_key, longitude, latitude, birding_data, zoomLevel) {

    mapboxgl.accessToken = api_key;
    // var longitude = {{ longitude }}
    // var latitude = {{ latitude }}
    map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/streets-v9', //stylesheet location
        center: [longitude, latitude], // starting position
        // center: [-121.403732, 40.492392],
        zoom: zoomLevel // starting zoom
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

    function filterBy(month) {
        var filters = ['==', 'month', months[month]];
        map.setFilter('bird_count', filters);
        // Set the label to the month
        document.getElementById('month').textContent = months[month];
    }

    // //Wait until the map loads before adding layers
    map.on('load', function () {
    //     // console.log(data.features)
        map.addSource("birding-locations", {
            "type": "geojson",
            "data": birding_data,
            "buffer": 25,
        });
        map.addLayer({
            'id': 'bird_count',
            'type': 'circle',
            'source': "birding-locations",
            'paint': {
                'circle-radius': {
                    property: 'obs_count',
                    stops: [
                        [0, 4],
                        [5, 9],
                        [10, 14],
                        [15, 19],
                        [20, 24],
                        [25, 29],
                    ]
                },
                'circle-color': {
                    property: 'obs_count',
                    stops: [
                      // ['X', '#000000'],
                      [0, '#2DC4B2'],
                      [1, '#3BB3C3'],
                      [2, '#669EC4'],
                      [3, '#8B88B6'],
                      [4, '#A2719B'],
                      [5, '#AA5E79']
                    ]
                },
                'circle-opacity': 0.8
            },
            'filter': ['!=', 'obs_count', 'X']
        }, 'admin-2-boundaries-dispute');

        map.addLayer({
            'id': 'x_count',
            'type': 'circle',
            'source': "birding-locations",
            'paint': {
                'circle-radius': 20,
                'circle-color': '#000000',
                'circle-opacity': 0.8
            },
            'filter': ['==', 'obs_count', 'X']
        }, 'admin-2-boundaries-dispute');
            
        filterBy(0);
        //Connect slider with map; gets the current month as an integer
        document.getElementById('slider').addEventListener('input', function(evt) {
            var month = parseInt(evt.target.value);
            filterBy(month);
        });
    });
    map.on('click', function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ['bird_count', 'x_count'] });
    if (!features.length) {
        return;
    }
    var feature = features[0];
    // Populate the popup and set its coordinates
    // based on the feature found.
    var popup = new mapboxgl.Popup()
        .setLngLat(feature.geometry.coordinates)
        .setHTML('Number of individuals reported: ' + feature.properties.obs_count)
        .addTo(map);
    });
    map.on('mousemove', function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ['bird_count', 'x_count'] });
        map.getCanvas().style.cursor = (features.length) ? 'pointer' : '';
    });
};

function getData() {
    $.get("/get_data.json", function(results) {
        var api_key = results.mapbox_api_key;
        var latitude = results.latitude;
        var longitude = results.longitude;
        var birding_data = results.birding_locations;
        var zoomLevel = results.zoomLevel;
        var bird_name = results.bird_name;
        changePicture(bird_name);
        // $("#map-loader").hide();
        // $("#map-row").show();
        renderMap(api_key, longitude, latitude, birding_data, zoomLevel);
        $("#map-loader").hide();
        $("#map-row").show();
    });
};

getData();

