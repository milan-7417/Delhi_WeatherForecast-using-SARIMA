async function loadForecast() {

    try {

        const response = await fetch("/forecast");

        const result = await response.json();

        if (!result.success) {

            alert(result.error);

            return;

        }

        const data = result.data;

        const current = data.current;

        // =====================================
        // Current Weather
        // =====================================

        document.getElementById("current-temp").innerHTML =
            `${current.temperature}°C`;

        document.getElementById("weather-description").innerHTML =
            current.description;

        // ==============================
// Date
// ==============================

        document.getElementById("current-date").innerHTML =
    new Date().toLocaleDateString("en-IN", {

        weekday: "long",

        day: "numeric",

        month: "long",

        year: "numeric"

    });


// ==============================
// Weather Update Time
// ==============================

        document.getElementById("weather-update").innerHTML =
    new Date(current.date).toLocaleTimeString("en-IN", {

        hour: "2-digit",

        minute: "2-digit"

    });

        document.getElementById("humidity").innerHTML =
            `${current.humidity}%`;

        document.getElementById("wind").innerHTML =
            `${current.wind_speed} km/h`;

        document.getElementById("pressure").innerHTML =
            `${current.pressure} hPa`;

        document.getElementById("sunrise").innerHTML =
            new Date(current.sunrise).toLocaleTimeString("en-IN", {
                hour: "2-digit",
                minute: "2-digit"
            });

        document.getElementById("sunset").innerHTML =
            new Date(current.sunset).toLocaleTimeString("en-IN", {
                hour: "2-digit",
                minute: "2-digit"
            });

        document.getElementById("aqi").innerHTML =
            current.aqi;

        document.getElementById("aqi-status").innerHTML =
            current.aqi_status;

        // =====================================
        // Forecast Cards
        // =====================================

        const container = document.getElementById("forecast");

        container.innerHTML = "";

        data.forecast.forEach(day => {

            container.innerHTML += `

            <div class="card">

                <h3>${new Date(day.date).toLocaleDateString("en-IN", {
                    weekday: "short",
                    day: "numeric",
                    month: "short"
                })}</h3>

                <p>🌡 <strong>Max:</strong> ${day.temperature_max} °C</p>

                <p>🌙 <strong>Min:</strong> ${day.temperature_min} °C</p>

                <p>🌤 <strong>Mean:</strong> ${day.temperature_mean} °C</p>

                <p>💧 <strong>Humidity:</strong> ${day.humidity}%</p>

                <p>🌧 <strong>Rain:</strong> ${day.precipitation} mm</p>

                <p>🌬 <strong>Wind:</strong> ${day.wind_speed} km/h</p>

                <p>☁ <strong>Cloud:</strong> ${day.cloud_cover}%</p>

                <p>🌡 <strong>Dew Point:</strong> ${day.dew_point} °C</p>

            </div>

            `;

        });

        // =====================================
        // Charts
        // =====================================

        window.forecastData = data.forecast;

        showChart(
          "temperature",
          document.querySelector(".chart-btn")
);

    }

    catch (error) {

        console.error("Error:", error);

    }

}

loadForecast();

function updateClock(){

    document.getElementById("live-time").innerHTML =
        new Date().toLocaleTimeString("en-IN",{

            hour:"2-digit",

            minute:"2-digit",

            second:"2-digit"

        });

}

updateClock();

setInterval(updateClock,1000);