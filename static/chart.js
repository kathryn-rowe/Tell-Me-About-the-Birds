"use strict"

var options = {
  responsive: true
};

var ctx_line = $("#lineChart").get(0).getContext("2d");

$.get("/bird_per_month.json", function (data) {
  var myLineChart = Chart.Line(ctx_line, {
                                data: data,
                                options: options
                            });
  $("#lineLegend").html(myLineChart.generateLegend());
});