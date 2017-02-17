"use strict"

var options = {
  responsive: true
};

var ctx_line = $("#lineChart").get(0).getContext("2d");

$.get("/melon-times.json", function (data) {
  var myLineChart = Chart.Line(ctx_line, {
                                data: data,
                                options: options
                            });
  $("#lineLegend").html(myLineChart.generateLegend());
});