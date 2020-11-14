var url = "/json_data";

function x_axis_size(array){
  new_array = [];
  for(i=0; i< array.length;i++){
    day_num = String(i+1);
    point = "Day" + day_num;
    new_array.push(point);
  }
  return new_array;
}

d3.json(url).then(function(response){
  var data = response;

  var x_axis = x_axis_size(data["Closing_Prices"])
  var y_axis = data["Closing_Prices"]

  var line_trace = {
    x: x_axis,
    y: y_axis,
    xaxis: 'x1',
    yaxis: 'y1',
    name: data["Company_Name"],
    type: "line",
    
  };


  console.log(data["positive"]);
  console.log(Number(data["positive"]));
  console.log(data["negative"]);
  console.log(Number(data["negative"]));
  var negative = Number(data["negative"])*100;
  var positive = Number(data["positive"])*100;
  var pie_data = [positive, negative];
  
    if (positive > negative) { 
        buysell = "Buy";
    }
      else {
        buysell= "Sell"
      };
   

  var pie_trace = {
    values:pie_data,
    labels: ["Positive", "Negative"],
    type: "pie",
    title: data["Company_Name"],
    titlefont: { size:20 },
    name: data["Company_Name"],
    marker: {
      colors: ['rgb(0, 0, 204)','rgb(255, 0, 0)']
    },
    domain: {
      x: [0, 0.48],
      y: [0, 0.98]
    }
  };

  var data1 = [pie_trace, line_trace];

  var layout = {
    title: buysell,
    titlefont: { size:50 },
    xaxis: {
      anchor: 'y2',
      domain: [0.52, 1]
    },
    yaxis: {
      anchor: 'x2',
      domain: [0, 0.98]
    }
  };


  Plotly.plot("myDiv", data1, layout);

})
