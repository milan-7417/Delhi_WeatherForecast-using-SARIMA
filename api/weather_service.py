import json
import requests
import pandas as pd

from datetime import datetime, timedelta
from pathlib import Path

from statsmodels.tsa.statespace.sarimax import SARIMAX

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_CONFIG = BASE_DIR / "models" / "model_config.json"

# =====================================================
# Delhi Coordinates
# =====================================================

LATITUDE = 28.6139
LONGITUDE = 77.2090

FORECAST_DAYS = 20

# =====================================================
# Weather Parameters
# =====================================================

WEATHER_COLUMNS = {

    "temperature_max": "temperature_2m_max",

    "temperature_min": "temperature_2m_min",

    "temperature_mean": "temperature_2m_mean",

    "humidity": "relative_humidity_2m_mean",

    "precipitation": "precipitation_sum",

    "wind_speed": "wind_speed_10m_max",

    "wind_direction": "wind_direction_10m_dominant",

    "pressure": "surface_pressure_mean",

    "cloud_cover": "cloud_cover_mean",

    "dew_point": "dew_point_2m_mean",

}

# ==========================================
# Air Quality
# ==========================================

def get_air_quality():

    url = (

        "https://air-quality-api.open-meteo.com/v1/air-quality"

        f"?latitude={LATITUDE}"

        f"&longitude={LONGITUDE}"

        "&current=us_aqi"

        "&timezone=Asia/Kolkata"

    )

    response = requests.get(url)

    response.raise_for_status()

    current = response.json()["current"]

    aqi = current["us_aqi"]

    if aqi <= 50:
        status = "Good"

    elif aqi <= 100:
        status = "Moderate"

    elif aqi <= 150:
        status = "Unhealthy"

    elif aqi <= 200:
        status = "Very Unhealthy"

    else:
        status = "Hazardous"

    return {

        "aqi": aqi,

        "status": status

    }

  


# =====================================================
# Current Weather
# =====================================================

def get_current_weather():

    url = (

    "https://api.open-meteo.com/v1/forecast"

    f"?latitude={LATITUDE}"

    f"&longitude={LONGITUDE}"

    "&current="

    "temperature_2m,"

    "relative_humidity_2m,"

    "surface_pressure,"

    "wind_speed_10m,"

    "apparent_temperature,"

    "weather_code,"

    "visibility"

    "&daily="

    "sunrise,sunset"

    "&timezone=Asia/Kolkata"

)

    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    current = response.json()["current"]
    daily = response.json()["daily"]
    air = get_air_quality()

    return {

    "date": current["time"],

    "temperature": current["temperature_2m"],

    "feels_like": current["apparent_temperature"],

    "humidity": current["relative_humidity_2m"],

    "pressure": current["surface_pressure"],

    "wind_speed": current["wind_speed_10m"],

    "weather_code": current["weather_code"],

    "description": WEATHER_CODES.get(

        current["weather_code"],

        "Unknown"

    ),

    "sunrise": daily["sunrise"][0],

    "sunset": daily["sunset"][0],

    "aqi": air["aqi"],

    "aqi_status": air["status"]

}
WEATHER_CODES = {

    0: "Clear Sky",

    1: "Mainly Clear",

    2: "Partly Cloudy",

    3: "Overcast",

    45: "Fog",

    48: "Depositing Rime Fog",

    51: "Light Drizzle",

    53: "Drizzle",

    55: "Dense Drizzle",

    61: "Light Rain",

    63: "Rain",

    65: "Heavy Rain",

    71: "Snow",

    80: "Rain Showers",

    95: "Thunderstorm"

}

# =====================================================
# Read Model Configuration
# =====================================================

def load_model_config():

    with open(

        MODEL_CONFIG,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


# =====================================================
# Download Historical Weather
# =====================================================

def download_historical_weather():

    end_date = datetime.today().date() - timedelta(days=1)

    start_date = end_date - timedelta(days=365 * 5)

    daily_parameters = ",".join(WEATHER_COLUMNS.values())

    url = (

        "https://archive-api.open-meteo.com/v1/archive"

        f"?latitude={LATITUDE}"

        f"&longitude={LONGITUDE}"

        f"&start_date={start_date}"

        f"&end_date={end_date}"

        f"&daily={daily_parameters}"

        "&timezone=Asia/Kolkata"

    )

    response = requests.get(

        url,

        timeout=30

    )

    response.raise_for_status()

    daily = response.json()["daily"]

    df = pd.DataFrame(daily)

    df.rename(

        columns={

            value: key

            for key, value in WEATHER_COLUMNS.items()

        },

        inplace=True

    )

    df["time"] = pd.to_datetime(df["time"])

    df.sort_values(

        "time",

        inplace=True

    )

    df.reset_index(

        drop=True,

        inplace=True

    )

    return df

# =====================================================
# Fit SARIMA
# =====================================================

def fit_sarima(

    series,

    order,

    seasonal_order

):

    model = SARIMAX(

        series,

        order=tuple(order),

        seasonal_order=tuple(seasonal_order),

        enforce_stationarity=False,

        enforce_invertibility=False,

    )

    fitted = model.fit(

        disp=False,

        maxiter=100

    )

    return fitted

# =====================================================
# Generate SARIMA Forecast
# =====================================================

def generate_sarima_forecast():

    df = download_historical_weather()

    configs = load_model_config()

    forecasts = {}

    for parameter in WEATHER_COLUMNS.keys():

        print(f"Forecasting {parameter}...")

        order = configs[parameter]["order"]

        seasonal_order = configs[parameter]["seasonal_order"]

        model = fit_sarima(

            df[parameter],

            order,

            seasonal_order

        )

        prediction = model.forecast(FORECAST_DAYS)

        forecasts[parameter] = prediction.tolist()

    return forecasts


# =====================================================
# Build Forecast Response
# =====================================================

from datetime import datetime, timedelta

from api.cache import (
    get_cache,
    update_cache,
)

CACHE_HOURS = 6


def generate_forecast():

    # -----------------------------------------
    # Check Cache
    # -----------------------------------------

    cache = get_cache()

    if (
        cache["data"] is not None
        and cache["generated_at"] is not None
        and (
            datetime.now() - cache["generated_at"]
        ).total_seconds() < CACHE_HOURS * 3600
    ):

        print("Using Cached Forecast...")

        return cache["data"]

    print("Generating New Forecast...")

    # -----------------------------------------
    # Current Weather
    # -----------------------------------------

    current_weather = get_current_weather()

    # -----------------------------------------
    # SARIMA Forecast
    # -----------------------------------------

    forecast_values = generate_sarima_forecast()

    # -----------------------------------------
    # Future Dates
    # -----------------------------------------

    future_dates = [

        (
            datetime.today().date()
            + timedelta(days=i)
        ).strftime("%Y-%m-%d")

        for i in range(1, FORECAST_DAYS + 1)

    ]

    # -----------------------------------------
    # Build Forecast
    # -----------------------------------------

    forecast = []

    for i in range(FORECAST_DAYS):

        row = {

            "date": future_dates[i]

        }

        for parameter in WEATHER_COLUMNS.keys():

            row[parameter] = round(

                float(
                    forecast_values[parameter][i]
                ),

                2

            )

        forecast.append(row)

    # -----------------------------------------
    # Final Result
    # -----------------------------------------

    result = {

        "generated_on": str(datetime.today().date()),

        "city": "Delhi",

        "current": current_weather,

        "forecast": forecast

    }

    # -----------------------------------------
    # Update Cache
    # -----------------------------------------

    update_cache(result)

    return result

