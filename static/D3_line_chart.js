"use strict"

var svg = d3.select("svg"),
    margin = {top: 10, right: 50, bottom: 10, left: 40},
    width = svg.attr("width") - margin.left - margin.right,
    height = svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// var parseTime = d3.timeParse("%Y%m%d");

    // setting the x&y axis, make sure that any quantity we specify on the x axis fits onto our graph.
     // By using the d3.time.scale() function we make sure that D3 knows to treat the values as month / time 
     // entities (with all their ingrained peculiarities). Then we specify the range that those values 
     // will cover (.range) and we specify the range as being from 0 to the width of our graphing area
var x = d3.scaleLinear().range([0, width]),
    y = d3.scaleLog().range([height, 0]),
    // setting the color
    z = d3.scaleOrdinal(d3.schemeCategory20b);

var line = d3.line()
    // Produces a cubic basis spline using the specified control points. 
    .curve(d3.curveBasis)
    // x value of the line is month
    .x(function(d) { return x(d.month); })
    // y value of the line is total
    .y(function(d) { return y(d.total); });


d3.json('/birds_per_month.json', function(error, data){
  if (error) throw error;
  var birds = data;


  // the .domain function is designed to let D3 know what the scope of the data will be this is what is 
  // then passed to the scale function. Find the min and max; returns an array.
  // x.domain(d3.extent(data, function(d) { console.log(d.month); return d.month; }));
  x.domain([
    d3.min(birds, function(c) { return d3.min(c.values, function(d) { return d.month; }); }),
    d3.max(birds, function(c) { return d3.max(c.values, function(d) { return d.month; }); })
  ]);

  y.domain([1,
    // d3.min(birds, function(c) { return d3.min(c.values, function(d) { return d.total; }); }),
    d3.max(birds, function(c) { return d3.max(c.values, function(d) { return d.total; }); })
  ]);
  
  z.domain(birds.map(function(c) { return c.id; }));

  // .call() invokes a callback function on the selection itself. D3’s call() function takes the incoming 
  // selection, as received from the prior link in the chain, and hands that selection off to any function. 
  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisTop(x));

  // labels for the Y axis
  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisRight(y));
   // .append("text")
   //    .attr("y", 10)
   //    .attr("dy", "0.1em")
   //    .attr("dx", "16em")
   //    .attr("fill", "#000")
   //    .style("font-size", "18")
   //    .style("font-style", "Roboto")
   //    .text("Bird species per month (log scale)");

  // this section displays the lines
  var bird = g.selectAll(".bird")
    .data(birds)
    .enter().append("g")
      .attr("class", "bird");
  
  // this section displays the lines
  bird.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", "#4a4a39" )
      .style("stroke-width", .5)
      .style("opacity", 1)
      .on("mouseover", mouseover)
      .on("mouseout", mouseout)
      .on("click", click);

  function mouseover(d, i) {
    d3.select(this).style("stroke", "#000000")
                   .style("stroke-width", 5); 
    $("#blurb").text(d.id);
  };

  function mouseout(d, i) {
    d3.select(this).style("stroke", "#4a4a39")
                   .style("stroke-width", .5);
    $("#blurb").html("&nbsp");
  };

  function click(d, i) {
    d3.select(this);
    var birdName = d.id;
    var centerMap = map.getCenter();
    var zoomLevel = map.getZoom();
    // console.log(centerMap.lat, centerMap.lng)
    // console.log(bird_name);
    $.ajax({
        url: "/reload_data.json",
        dataType: 'json',
        type: 'GET',
        data: {"bird": birdName},
        success: function(results) {
            var api_key = results.mapbox_api_key;
            var latitude = centerMap.lat;
            var longitude = centerMap.lng;
            var birding_data = results.birding_locations;
            var bird_name = results.bird_name;
            var county_name = results.county_name;
            changePicture(bird_name);
            renderMap(api_key, longitude, latitude, birding_data, zoomLevel);
            $('.map-overlay-inner').empty();
            $('.map-overlay-inner').html("<h2>"+bird_name + " Observations in " + county_name + " County, 2015</h2><label for='slider' id='month'>January</label><input id='slider' type='range' min='0' max='11' step='1' value='0' />");   
        }
    });
  }
}); 
