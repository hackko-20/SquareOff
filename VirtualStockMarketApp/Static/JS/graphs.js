function openGraph(evt, GraphID)
{
    let graphs = document.getElementsByClassName('graph');
    for(let i = 0; i < graphs.length; i++)
    {
        graphs[i].style.display = "none";
    }
    document.getElementById(GraphID).style.display = "block";
}

am4core.useTheme(am4themes_animated);

let chart = am4core.create("Candlestick", am4charts.XYChart);
chart.paddingRight = 20;

chart.dateFormatter.inputDateFormat = "k:m";

let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
dateAxis.renderer.grid.template.location = 0;
dateAxis.renderer.minGridDistance = 60;
dateAxis.groupData = true;
dateAxis.start = 0.95;
dateAxis.end = 1;
dateAxis.keepSelection = true;

let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.tooltip.disabled = true;

let series = chart.series.push(new am4charts.CandlestickSeries());
series.dataFields.dateX = "minute";
series.dataFields.valueY = "close";
series.dataFields.openValueY = "open";
series.dataFields.lowValueY = "low";
series.dataFields.highValueY = "high";
series.groupFields.valueY = "average";
series.groupFields.openValueY = "average";
series.groupFields.lowValueY = "average";
series.groupFields.highValueY = "average";
series.tooltipText = "Open: [bold]${openValueY.value}[/]\nLow: [bold]${lowValueY.value}[/]\nHigh: [bold]${highValueY.value}[/]\nClose: [bold]${valueY.value}[/]";

chart.cursor = new am4charts.XYCursor();

chart.scrollbarX = new am4core.Scrollbar();


const apikey = "pk_245073c85596466aa6afff012f007125";
let url = "https://cloud.iexapis.com/" + "stable/stock/" + symbol + "/intraday-prices/quote?token=" + apikey + "&filter=minute,high,low,open,close";
console.log(url);
chart.dataSource.url = url;

//   "date": "2018-10-16",
//   "open": "172.69",
//   "high": "173.04",
//   "low": "169.18",
//   "close": "172.75"

let chartLG = am4core.create("Line", am4charts.XYChart);

let dateAxisLG = chartLG.xAxes.push(new am4charts.DateAxis());
dateAxisLG.renderer.grid.template.location = 0;
dateAxisLG.renderer.minGridDistance = 60;
// dateAxisLG.start = 0.95;
// dateAxisLG.end = 1;
// dateAxisLG.keepSelection = true;

let valueAxisLG = chartLG.yAxes.push(new am4charts.ValueAxis());
valueAxisLG.tooltip.disabled = true;

chartLG.dateFormatter.inputDateFormat = "k:m";
dateAxisLG.groupData = true;

let seriesLG = chartLG.series.push(new am4charts.LineSeries());
seriesLG.dataFields.dateX = "minute";
seriesLG.dataFields.valueY = "average";
//seriesLG.groupFields.valueY = "average";
seriesLG.tooltipText = "Average: [bold]${valueY.value}[/]";

let urlLG = "https://cloud.iexapis.com/" + "stable/stock/" + symbol + "/intraday-prices/quote?token=" + apikey + "&filter=minute,average";
chartLG.dataSource.url = urlLG;
console.log(urlLG);

chartLG.cursor = new am4charts.XYCursor();

chartLG.scrollbarX = new am4core.Scrollbar();

let chartBG = am4core.create("Bar", am4charts.XYChart);
let dateAxisBG = chartBG.xAxes.push(new am4charts.DateAxis());
dateAxisBG.renderer.grid.template.location = 0;
dateAxisBG.renderer.minGridDistance = 60;
dateAxisBG.groupData = true;
// dateAxisBG.start = 0.95;
// dateAxisBG.end = 1;
// dateAxisBG.keepSelection = true;

let valueAxisBG = chartBG.yAxes.push(new am4charts.ValueAxis());
valueAxisBG.tooltip.disabled = true;
chartBG.dateFormatter.inputDateFormat = "k:m";

let seriesBG = chartBG.series.push(new am4charts.OHLCSeries());
seriesBG.dataFields.dateX = "minute";
seriesBG.dataFields.valueY = "close";
seriesBG.dataFields.openValueY = "open";
seriesBG.dataFields.lowValueY = "low";
seriesBG.dataFields.highValueY = "high";
// seriesBG.groupFields.valueY = "average";
// seriesBG.groupFields.openValueY = "average";
// seriesBG.groupFields.lowValueY = "average";
// seriesBG.groupFields.highValueY = "average";
seriesBG.tooltipText = "Open: [bold]${openValueY.value}[/]\nLow: [bold]${lowValueY.value}[/]\nHigh: [bold]${highValueY.value}[/]\nClose: [bold]${valueY.value}[/]";

chartBG.dataSource.url = url;
chartBG.cursor = new am4charts.XYCursor();

chartBG.scrollbarX = new am4core.Scrollbar();