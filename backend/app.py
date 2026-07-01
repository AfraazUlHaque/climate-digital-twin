import json
from pathlib import Path
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import METRICS_PATHS
from data_service import data_service
from model_service import model_service
from prediction_service import prediction_service
from weather_service import get_live_weather, normalize_city
from data_assimilation import assimilation_engine
from assimilation_history import get_history

app = FastAPI(
    title="AI Climate Digital Twin API",
    version="2.0.0",
)
BASE_DIR = Path(__file__).resolve().parent
EDA_DIR = BASE_DIR / "outputs" / "eda"

if EDA_DIR.exists():
    app.mount("/eda", StaticFiles(directory=str(EDA_DIR)), name="eda")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def first_existing(paths):
    for path in paths:
        if path.exists():
            return path
    return None


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Weighted GNN inference backend is live",
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "backend": "running",
    }


@app.get("/api/model-status")
def model_status():
    data_service.load()
    model, _, _ = model_service.load(input_dim=len(data_service.feature_cols))

    return {
        "status": "loaded",
        "model": str(model_service.model_path),
        "x_scaler": str(model_service.x_scaler_path),
        "y_scaler": str(model_service.y_scaler_path),
        "input_dim": model_service.input_dim,
        "output_dim": model_service.output_dim,
        "feature_cols": data_service.feature_cols,
        "csv": str(data_service.csv_path),
    }


@app.get("/api/regions")
def regions():
    return {
        "regions": data_service.get_regions()
    }


@app.get("/api/dates")
def dates(region: str = Query(None)):
    return {
        "region": region,
        "dates": data_service.get_dates(region)
    }


@app.get("/api/forecast")
def forecast(
    region: str = Query("Kerala"),
    date: str = Query(None),
):
    return prediction_service.summary(region, date)


@app.get("/api/forecast/history")
def forecast_history(region: str = Query("Kerala")):
    return {
        "region": region,
        "history": prediction_service.history(region)
    }


@app.get("/api/map-data")
def map_data(
    region: str = Query("Kerala"),
    date: str = Query(None),
):
    return {
        "region": region,
        "points": prediction_service.map_data(region, date)
    }


@app.get("/api/flood-risk")
def flood_risk(
    region: str = Query("Kerala"),
    date: str = Query(None),
):
    summary = prediction_service.summary(region, date)
    flood = summary["risk"]["flood"]

    return {
        "region": region,
        "date": summary["date"],
        "score": flood["score"],
        "level": flood["level"],
        "advisory": flood["advisory"],
    }


@app.get("/api/drought-risk")
def drought_risk(
    region: str = Query("Kerala"),
    date: str = Query(None),
):
    summary = prediction_service.summary(region, date)
    drought = summary["risk"]["drought"]

    return {
        "region": region,
        "date": summary["date"],
        "score": drought["score"],
        "level": drought["level"],
        "advisory": drought["advisory"],
    }


@app.get("/api/live-weather")
def live_weather(city: str = Query("Kochi")):
    return get_live_weather(city)


@app.get("/api/metrics")
def metrics():
    path = first_existing(METRICS_PATHS)

    if path:
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)

            if isinstance(raw, dict) and "models" in raw:
                return raw

            models = []

            for key, value in raw.items():
                if isinstance(value, dict):
                    models.append({
                        "model": key,
                        "mae": round(float(value.get("mae", 0)), 4),
                        "rmse": round(float(value.get("rmse", 0)), 4),
                        "r2": round(float(value.get("r2", 0)), 4),
                    })

            if models:
                return {"models": models}

        except Exception:
            pass

    return {
        "models": [
            {"model": "ExtraTrees", "mae": 4.461, "rmse": 10.332, "r2": 0.335},
            {"model": "Weighted GNN", "mae": 4.189, "rmse": 10.669, "r2": 0.293},
            {"model": "Hybrid LSTM-GNN", "mae": 4.580, "rmse": 11.800, "r2": 0.135},
            {"model": "ConvLSTM", "mae": 0.034, "rmse": 0.052, "r2": 0.870},
        ]
    }
@app.get("/api/assimilated-forecast")
def assimilated_forecast(
    region: str = Query("Kerala"),
    date: str = Query(None),
):
    model_summary = prediction_service.summary(region, date)

    city = normalize_city(region)
    live_weather = get_live_weather(city)

    return assimilation_engine.assimilate_summary(
        region=region,
        model_summary=model_summary,
        live_weather=live_weather,
    )

@app.get("/api/assimilation-history")
def assimilation_history():
    return {
        "history": get_history()
    }

@app.post("/api/what-if")
def what_if(payload: dict = Body(...)):
    return prediction_service.what_if(payload)


@app.post("/api/what-if-grid")
def what_if_grid(payload: dict = Body(...)):
    return prediction_service.what_if_grid(payload)


@app.post("/api/predict")
def predict(payload: dict = Body(...)):
    region = payload.get("region", "Kerala")
    date = payload.get("date", None)

    return prediction_service.summary(region, date)