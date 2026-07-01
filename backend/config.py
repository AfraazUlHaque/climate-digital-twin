from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent

DEVICE = "cpu"

MODEL_PATHS = [
    BACKEND_DIR / "outputs" / "models" / "weighted_gnn_best.pt",
    BACKEND_DIR / "models" / "weighted_gnn_best.pt",
    ROOT_DIR / "models" / "weighted_gnn_best.pt",
]

X_SCALER_PATHS = [
    BACKEND_DIR / "outputs" / "models" / "weighted_gnn_x_scaler.pkl",
    BACKEND_DIR / "models" / "weighted_gnn_x_scaler.pkl",
    ROOT_DIR / "models" / "weighted_gnn_x_scaler.pkl",
]

Y_SCALER_PATHS = [
    BACKEND_DIR / "outputs" / "models" / "weighted_gnn_y_scaler.pkl",
    BACKEND_DIR / "models" / "weighted_gnn_y_scaler.pkl",
    ROOT_DIR / "models" / "weighted_gnn_y_scaler.pkl",
]

GRAPH_PATHS = [
    BACKEND_DIR / "outputs" / "models" / "climate_graphs_weighted.pt",
    BACKEND_DIR / "outputs" / "climate_graphs_weighted.pt",
    BACKEND_DIR / "data" / "climate_graphs_weighted.pt",
    ROOT_DIR / "data" / "processed" / "graphs" / "climate_graphs_weighted.pt",
]

PREDICTION_CSV_PATHS = [
    BACKEND_DIR / "outputs" / "weighted_gnn_predictions.csv",
    ROOT_DIR / "outputs" / "weighted_gnn_predictions.csv",
    ROOT_DIR / "outputs" / "predictions" / "weighted_gnn_predictions.csv",
]

METRICS_PATHS = [
    BACKEND_DIR / "outputs" / "weighted_gnn_metrics.json",
    BACKEND_DIR / "outputs" / "metrics" / "weighted_gnn_metrics.json",
    ROOT_DIR / "outputs" / "metrics" / "weighted_gnn_metrics.json",
]

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

CITY_COORDS = {
    "Kochi": {"lat": 9.9312, "lon": 76.2673, "region": "Kerala"},
    "Kozhikode": {"lat": 11.2588, "lon": 75.7804, "region": "Kerala"},
    "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366, "region": "Kerala"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "region": "Tamil Nadu"},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "region": "Tamil Nadu"},
    "Madurai": {"lat": 9.9252, "lon": 78.1198, "region": "Tamil Nadu"},
}