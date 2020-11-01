function openForm(evt, divisionName ) {
    var i, divisionElement, tablinks;
    divisionElement = document.getElementsByClassName("commonElements");
    for (i = 0; i < divisionElement.length; i++) {
        divisionElement[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(divisionName).style.display = "block";
    evt.currentTarget.className += " active";
}

function openDiv( divisionName ) {
    var i, divisionElement;
    divisionElement = document.getElementsByClassName("subClass");
    for (i = 0; i < divisionElement.length; i++) {
        divisionElement[i].style.display = "none";
    }
    document.getElementById(divisionName).style.display = "block";
}

function myFunction() {
    var x = document.getElementById("myLinks");
    if (x.style.display === "block") 
    {
        x.style.display = "none";
    }
    else 
    {
          x.style.display = "block";
    }
}

let chartLG = am4core.create("statusGraph", am4charts.XYChart);

let dateAxisLG = chartLG.xAxes.push(new am4charts.DateAxis());
dateAxisLG.renderer.grid.template.location = 0;
dateAxisLG.renderer.minGridDistance = 60;

let valueAxisLG = chartLG.yAxes.push(new am4charts.ValueAxis());
valueAxisLG.tooltip.disabled = true;

chartLG.dateFormatter.inputDateFormat = "yyyy-mm-dd";
dateAxisLG.groupData = true;

let seriesLG = chartLG.series.push(new am4charts.LineSeries());
seriesLG.dataFields.dateX = "minute";
seriesLG.dataFields.valueY = "average";
seriesLG.groupFields.valueY = "average";
seriesLG.tooltipText = "Average: [bold]${valueY.value}[/]";

chartLG.dataSource.url = 'chart/getdata'
chartLG.dataSource.parser = new am4core.JSONParser();

chartLG.cursor = new am4charts.XYCursor();

chartLG.scrollbarX = new am4core.Scrollbar();

var labels=[];
var values=[];
var endpoint = '/chart/getdata'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(datagone){
    console.log(datagone)
    labels=datagone.labels
    values=datagone.values
        var ctx = document.getElementById('statusGraph').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: labels ,
              datasets: [{
                label: 'Profit',
                data: values ,
                backgroundColor: [
                    'rgba(255, 99, 132, 1)',                  
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',            
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        });
    },
})   

let api_key = "pk_245073c85596466aa6afff012f007125";
let url = "https://cloud.iexapis.com/" + "stable/stock/" + symbol + "/quote?token=" + api_key;
fetch(url)
    .then(response => response.json())
    .then(data => {
            console.log("in data");
            var x=data.latestPrice;
            document.getElementById("stock_symbolCol").innerHTML = x;
    })
    .catch(error => {
        alert("stock symbol not found");
});
