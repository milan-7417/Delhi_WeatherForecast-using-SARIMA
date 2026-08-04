let weatherChart = null;

// ======================================
// Chart
// ======================================

function showChart(type, button = null) {

    document.querySelectorAll(".chart-btn").forEach(btn => {

        btn.classList.remove("active");

    });

    if (button) {

        button.classList.add("active");

    }
    else {

        const buttons = document.querySelectorAll(".chart-btn");

        switch (type) {

            case "temperature":
                buttons[0].classList.add("active");
                break;

            case "rain":
                buttons[1].classList.add("active");
                break;

            case "humidity":
                buttons[2].classList.add("active");
                break;

            case "wind":
                buttons[3].classList.add("active");
                break;

        }

    }

    drawChart(type);

}


// ======================================
// Draw Selected Chart
// ======================================

function drawChart(type) {

    const forecast = window.forecastData;

    if (!forecast) return;

    const labels = forecast.map(day =>

        new Date(day.date).toLocaleDateString("en-IN", {

            day: "numeric",

            month: "short"

        })

    );

    let values = [];

    let label = "";

    let chartType = "line";

    let borderColor = "#1565c0";

    let backgroundColor = "rgba(21,101,192,0.15)";

    switch (type) {

        case "temperature":

            values = forecast.map(day => day.temperature_mean);

            label = "Temperature (°C)";

            chartType = "line";

            borderColor = "#e53935";

            backgroundColor = "rgba(229,57,53,.15)";

            break;

        case "rain":

            values = forecast.map(day => day.precipitation);

            label = "Rainfall (mm)";

            chartType = "bar";

            borderColor = "#1e88e5";

            backgroundColor = "rgba(30,136,229,.75)";

            break;

        case "humidity":

            values = forecast.map(day => day.humidity);

            label = "Humidity (%)";

            chartType = "line";

            borderColor = "#26a69a";

            backgroundColor = "rgba(38,166,154,.15)";

            break;

        case "wind":

            values = forecast.map(day => day.wind_speed);

            label = "Wind Speed (km/h)";

            chartType = "line";

            borderColor = "#8e24aa";

            backgroundColor = "rgba(142,36,170,.15)";

            break;

    }

    if (weatherChart) {

        weatherChart.destroy();

    }

    const ctx = document
        .getElementById("weatherChart")
        .getContext("2d");

    weatherChart = new Chart(ctx, {

        type: chartType,

        data: {

            labels: labels,

            datasets: [{

                label: label,

                data: values,

                borderColor: borderColor,

                backgroundColor: backgroundColor,

                borderWidth: 3,

                fill: chartType === "line",

                tension: 0.4,

                pointRadius: 4,

                pointHoverRadius: 7

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            animation: {

                duration: 1000

            },

            interaction: {

                intersect: false,

                mode: "index"

            },

            plugins: {

                legend: {

                    display: true,

                    position: "top",

                    labels: {

                        font: {

                            size: 14,

                            weight: "bold"

                        }

                    }

                },

                tooltip: {

                    enabled: true

                }

            },

            scales: {

                x: {

                    grid: {

                        display: false

                    }

                },

                y: {

                    beginAtZero: false,

                    grid: {

                        color: "#eeeeee"

                    }

                }

            }

        }

    });

}