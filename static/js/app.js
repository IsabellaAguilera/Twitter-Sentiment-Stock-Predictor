
function buildPredictionPlot(){

    var url = "/company"

    d3.json(url).then(function(response) {
        var data = response;

        var twitterPercentages = data.map(function(record) {
            return record[''];
        });

        var stockPrices = data.map(function(record) {
            return record[''];
        });

        var stockDays = data.map(function(record) {
            return record[''];
        });

        var pieColors = ['rgb(255, 0, 0)','rgb(0, 0, 238)'];

        var trace1 = {
            values: twitterPercentages,
            labels: ["% of Positive Tweets", "% of Negative Tweets"],
            type: "pie",
            marker: {
                colors: pieColors
            }
        };

        var trace2 = {
            x: stockDays,
            y: stockPrices,
            type: "line",


        };

        var layout1 = {
            showlegend: true,
            title: "Twitter Positive/Negative Percentagas"

        };

        var layout2 = {
            showlegend: true,
            title: "Stock Closing Price Over 7 Days"
        };

        var data1 = [trace1];
        var data2 = [trace2];

        Plotly.plot("pie", data1, layout1);
        Plotly.plot("line", data2, layout2);

    });

};

function buySell() {

    var value = data.map(function(record) {
        return record[''];
    });

    if(value === 1){
        $("div#buysell").append('Buy');
    }
    else{
        $("div#buysell").append('Sell');
    }

};