from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.weather_service import generate_forecast

from contextlib import asynccontextmanager

from api.weather_service import generate_forecast

# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# FastAPI App
# ==========================================

@asynccontextmanager
async def lifespan(app):

    print("Loading Forecast...")

    generate_forecast()

    print("Forecast Ready")

    yield


app = FastAPI(

    title="Delhi Weather Forecast",

    lifespan=lifespan

)

# ==========================================
# Templates
# ==========================================

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

# ==========================================
# Static Files
# ==========================================

app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static"
)

# ==========================================
# Home Page
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )

# ==========================================
# Weather Forecast API
# ==========================================

@app.get("/forecast")
async def forecast():

    try:

        data = generate_forecast()

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

# ==========================================
# Health Check
# ==========================================

@app.get("/health")
async def health():

    return {
        "status": "running",
        "application": "Delhi Weather Forecast API"
    }