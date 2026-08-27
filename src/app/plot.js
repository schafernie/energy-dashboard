console.log("The plot is evolving!")


document.getElementById('start_date').value = '2026-01-01';//initiaze start and end date
document.getElementById('end_date').value = '2026-01-07';


async function plot(){
    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const response = await fetch(`/api/load?start_date=${startDate}&end_date=${endDate}`);
    const data = await response.json();
    Plotly.newPlot("plot", [
        { x: data.total_consumption.date_time, y: data.total_consumption.value_mwh, name: "Actual", type: "scatter", mode: "lines" },
    ], {
    xaxis: {title: "Time" },
    yaxis: {title: "Total Consumption (MWh)"},
    });
}


plot();

document.getElementById('start_date').addEventListener('change', plot);
document.getElementById('end_date').addEventListener('change', plot);



