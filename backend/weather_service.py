import requests
from fastapi import HTTPException

from config import CITY_COORDS, OPEN_METEO_URL


REGION_CITY_MAP = {
    "Kerala": "Kochi",
    "Tamil Nadu": "Chennai",
}


def normalize_city(city):
    city = city or "Kochi"

    if city in REGION_CITY_MAP:
        return REGION_CITY_MAP[city]

    return city


def get_live_weather(city):
    city = normalize_city(city)

    if city not in CITY_COORDS:
        raise HTTPException(status_code=404, detail=f"Unsupported city: {city}")

    loc = CITY_COORDS[city]

    params = {
        "latitude": loc["lat"],
        "longitude": loc["lon"],
        "current": "temperature_2m,precipitation,relative_humidity_2m,wind_speed_10m",
        "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
    }

    try:
        res = requests.get(OPEN_METEO_URL, params=params, timeout=15)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather API failed: {str(e)}")

    current = data.get("current", {})
    daily = data.get("daily", {})

    return {
        "city": city,
        "region": loc["region"],
        "lat": loc["lat"],
        "lon": loc["lon"],
        "current": {
            "temperature": current.get("temperature_2m", 0),
            "precipitation": current.get("precipitation", 0),
            "humidity": current.get("relative_humidity_2m", 0),
            "wind_speed": current.get("wind_speed_10m", 0),
        },
        "daily": daily,
    }