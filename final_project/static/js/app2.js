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
  var line_trace = {
    x: x_axis,
    y: data["Closing_Prices"],
    name: data["Company_Name"],
    type: "line"
  };
  console.log(data["positive"]);
  console.log(Number(data["positive"]));
  console.log(data["negative"]);
  console.log(Number(data["negative"]));
  var negative = Number(data["negative"])*100;
  var positive = Number(data["positive"])*100;
  var pie_data = [positive, negative];

  var pie_trace = {
    values:pie_data,
    labels: ["Positive", "Negative"],
    type: "pie"
  }

  var layout = {
    title: data["Company_Name"],
  };

// Need a Visual for the Buy or sell=> Data is in data['prediction']

  Plotly.plot("line", [line_trace], layout);
  Plotly.plot("pie", [pie_trace], layout);

})
