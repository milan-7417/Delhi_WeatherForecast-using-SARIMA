from datetime import datetime

forecast_cache = {

    "generated_at": None,

    "data": None

}


def get_cache():

    return forecast_cache


def update_cache(data):

    forecast_cache["generated_at"] = datetime.now()

    forecast_cache["data"] = data