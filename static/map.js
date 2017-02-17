"use strict"
function renderMap(api_key, longitude, latitude, birding_data){

    mapboxgl.accessToken = api_key;
    // var longitude = {{ longitude }}
    // var latitude = {{ latitude }}
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
    function filterBy(month) {
        var filters = ['==', 'month', months[month]];
        map.setFilter('obs_count', filters);
        // Set the label to the month
        document.getElementById('month').textContent = months[month];
    }

    // //Wait until the map loads before adding layers
    map.on('load', function () {
    //     // console.log(data.features)
        map.addSource("birding-locations", {
            "type": "geojson",
            "data": birding_data,
        });
        map.addLayer({
            'id': 'obs_count',
            'type': 'circle',
            'source': "birding-locations",
            'paint': {
                'circle-radius': {
                    property: 'obs_count',
                    stops: [
                        [0, 5],
                        [10, 35]
                    ]
                },
                'circle-color': {
                    property: 'obs_count',
                    stops: [
                      [0, '#2DC4B2'],
                      [1, '#3BB3C3'],
                      [2, '#669EC4'],
                      [3, '#8B88B6'],
                      [4, '#A2719B'],
                      [5, '#AA5E79']
                    ]
                },
                'circle-opacity': 0.8
            }
        }, 'admin-2-boundaries-dispute');
    //         }, 'waterway-label');
            
        filterBy(0);
    //     //Connect slider with map; gets the current month as an integer
        document.getElementById('slider').addEventListener('input', function(evt) {
            var month = parseInt(evt.target.value);
            filterBy(month);
        });
    });
    map.on('click', function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ['obs_count'] });
    if (!features.length) {
        return;
    }
    var feature = features[0];
    // Populate the popup and set its coordinates
    // based on the feature found.
    var popup = new mapboxgl.Popup()
        .setLngLat(feature.geometry.coordinates)
        .setHTML('Number of species reported: ' + feature.properties.obs_count)
        .addTo(map);
    });
    map.on('mousemove', function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ['obs_count'] });
        map.getCanvas().style.cursor = (features.length) ? 'pointer' : '';
    });
};


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