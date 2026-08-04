from pathlib import Path

# ===========================
# Project Paths
# ===========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

FORECAST_DIR = BASE_DIR / "forecast"

RAW_DATA = DATA_DIR / "delhi_weather.csv"

CLEAN_DATA = DATA_DIR / "clean_weather.csv"

FORECAST_JSON = FORECAST_DIR / "forecast.json"

MODELS_DIR = BASE_DIR / "models"
# ===========================
# Dataset Columns
# ===========================

DATE_COLUMN = "time"

WEATHER_COLUMNS = [
    "temperature_max",
    "temperature_min",
    "temperature_mean",
    "humidity",
    "precipitation",
    "wind_speed",
    "wind_direction",
    "pressure",
    "cloud_cover",
    "dew_point",
]

# ===========================
# Forecast Settings
# ===========================

FORECAST_DAYS = 20