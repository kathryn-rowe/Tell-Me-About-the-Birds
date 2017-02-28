"use strict"

var svg = d3.select("svg"),
    margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = svg.attr("width") - margin.left - margin.right,
    height = svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// var parseTime = d3.timeParse("%Y%m%d");

    // setting the x&y axis, make sure that any quantity we specify on the x axis fits onto our graph.
     // By using the d3.time.scale() function we make sure that D3 knows to treat the values as date / time 
     // entities (with all their ingrained peculiarities). Then we specify the range that those values 
     // will cover (.range) and we specify the range as being from 0 to the width of our graphing area
var x = d3.scaleLinear().range([0, width]),
    y = d3.scaleLinear().range([height, 0]),
    // setting the color
    z = d3.scaleOrdinal(d3.schemeCategory10);

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

// console.log(birds);
// });

// d3.csv('static/data.csv', type, function(error, data) {
  
//   if (error) throw error;

//   var cities = data.columns.slice(1).map(function(id) {
//     return {
//       id: id,
//       values: data.map(function(d) {
//         return {date: d.date, temperature: d[id]};
//       })
//     };
//   });
//   console.log(cities);
  // console.log(data);


  // the .domain function is designed to let D3 know what the scope of the data will be this is what is 
  // then passed to the scale function. Find the min and max; returns an array.
  x.domain(d3.extent(data, function(d) { return d.month; }));
  
  y.domain([
    d3.min(birds, function(c) { return d3.min(c.values, function(d) { return d.total; }); }),
    d3.max(birds, function(c) { return d3.max(c.values, function(d) { return d.total; }); })
  ]);
  
  z.domain(birds.map(function(c) { return c.id; }));

  // .call() invokes a callback function on the selection itself. D3’s call() function takes the incoming 
  // selection, as received from the prior link in the chain, and hands that selection off to any function. 
  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));
  debugger;
  // labels for the Y axis
  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))
   .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.90em")
      .attr("fill", "#000")
      .text("This is the Y axis");

  // this section displays the lines
  var bird = g.selectAll(".bird")
    .data(birds)
    .enter().append("g")
      .attr("class", "bird");
  
  // this section displays the lines
  bird.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return z(d.id); });
  
//   // thid section labels the lines on the graph
  bird.append("text")
      .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.month) + "," + y(d.value.total) + ")"; })
      .attr("x", 3)
      .attr("dy", "0.35em")
      .style("font", "10px sans-serif")
      .text(function(d) { return d.id; });
});

// function used to parse csv file
// function type(d, _, columns) {
//   d.date = parseTime(d.date);
//   // for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
//   return d;
// }
