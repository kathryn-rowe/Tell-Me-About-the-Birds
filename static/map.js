"use strict"

var map;

function renderMap(api_key, longitude, latitude, birding_data, zoomLevel) {

    mapboxgl.accessToken = api_key;

    map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/light-v9', //stylesheet location
        center: [longitude, latitude], // starting position
        zoom: zoomLevel, // starting zoom
        maxZoom: 12
    });
    
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
                        [20, 6],
                        [40, 9],
                        [60, 12],
                        [80, 15],
                    ]
                },
                'circle-color': {
                    property: 'obs_count',
                    stops: [
                      // ['X', '#000000'],
                      [10, '#f29e00'],
                      [15, '#f29e00'],
                      [25, '#f29e00'],
                      [30, '#f29e00'],
                    ]
                },
                'circle-opacity': 0.9,
                'circle-stroke-width': 1 ,
                'circle-stroke-color': '#bc7c04'
            },
            'filter': ['!=', 'obs_count', 'X']
        }, 'admin-2-boundaries-dispute');

        // map.addLayer({
        //     'id': 'x_count',
        //     'type': 'circle',
        //     'source': "birding-locations",
        //     'paint': {
        //         'circle-radius': 1,
        //         'circle-color': '#ffffff',
        //         'circle-opacity': 1
        //     },
        //     'filter': ['==', 'obs_count', 'X']
        // }, 'admin-2-boundaries-dispute');
            
        filterBy(0);
        //Connect slider with map; gets the current month as an integer
        document.getElementById('slider').addEventListener('input', function(evt) {
            var month = parseInt(evt.target.value);
            filterBy(month);
        });
    });
    map.on('click', function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ['bird_count'] });
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
        var features = map.queryRenderedFeatures(e.point, { layers: ['bird_count'] });
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
        renderMap(api_key, longitude, latitude, birding_data, zoomLevel);
        $("#map-loader").hide();
        // $("#map-row").show();
    });
};

getData();

