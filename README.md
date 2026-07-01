# 🌍 AI Climate Digital Twin

An AI-powered Climate Digital Twin that forecasts rainfall, estimates flood and drought risk, performs real-time scenario simulations, and integrates live weather observations through Data Assimilation. The platform is built using a trained Weighted Graph Neural Network (Weighted GNN) and provides an interactive GIS dashboard for climate intelligence.

---

# 🚀 Features

## 🤖 AI Prediction Engine
- Trained Weighted Graph Neural Network (Weighted GNN)
- Multi-day rainfall forecasting
- Flood Risk Prediction
- Drought Risk Prediction

## 🌦 Live Weather Integration
- Open-Meteo API integration
- Real-time weather observations
- Temperature
- Humidity
- Wind Speed
- Cloud Cover

## 🔄 Data Assimilation
- Combines AI model predictions with live observations
- Continuously updates forecasts
- Adaptive climate prediction

## 🛰 Digital Twin Dashboard
- Live Climate Dashboard
- Interactive GIS Map
- Forecast Visualization
- KPI Cards
- Historical Trends
- Risk Gauges

## 🌧 What-if Simulator
Users can simulate climate scenarios by changing:

- Rainfall
- Temperature

The system instantly updates:

- Rainfall Forecast
- Flood Risk
- Drought Risk
- Spatial Risk Map

## 📊 Climate Analytics
- Monthly Rainfall Trends
- Daily Rainfall Trends
- Monthly Temperature Trends
- Daily Temperature Trends
- Rainfall Distribution
- Temperature Distribution
- Correlation Matrix
- Regional Climate Summary

---

# 🏗 System Architecture

```
                     Live Weather API
                           │
                           ▼
                  Data Assimilation Engine
                           │
                           ▼
        Climate Dataset → Weighted GNN Model
                           │
                           ▼
               Prediction & Risk Engine
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
         ▼                                   ▼
   Dashboard                         What-if Simulator
         │                                   │
         └───────────────┬───────────────────┘
                         ▼
                  Interactive GIS Map
```

---

# 💻 Tech Stack

## Backend

- FastAPI
- PyTorch
- NumPy
- Pandas
- Scikit-Learn
- Open-Meteo API

## Frontend

- React
- Vite
- Axios
- Recharts
- React Leaflet

---

# 📂 Project Structure

```
AI-Climate-Digital-Twin
│
├── backend
│   ├── app.py
│   ├── prediction_service.py
│   ├── model_service.py
│   ├── data_service.py
│   ├── weather_service.py
│   ├── data_assimilation.py
│   ├── risk_engine.py
│   ├── outputs
│   │   ├── models
│   │   └── eda
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── api
│   │   ├── components
│   │   ├── pages
│   │   ├── styles
│   │   └── App.jsx
│   └── package.json
│
└── README.md
```

---

# ⚙ Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python -m uvicorn app:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

API Documentation:

```
http://127.0.0.1:8000/docs
```

---

# ⚙ Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# 🔌 API Endpoints

| Method | Endpoint |
|----------|---------------------------|
| GET | /api/health |
| GET | /api/model-status |
| GET | /api/regions |
| GET | /api/forecast |
| GET | /api/forecast/history |
| GET | /api/map-data |
| GET | /api/live-weather |
| GET | /api/metrics |
| GET | /api/assimilated-forecast |
| POST | /api/what-if |
| POST | /api/what-if-grid |

---

# 🧠 Data Assimilation

The Digital Twin continuously updates model forecasts using live weather observations.

```
Assimilated Forecast

=

Weighted GNN Prediction

+

Live Weather Correction
```

This allows the platform to adapt predictions according to real-time atmospheric conditions.

---

# 🌍 Regions Supported

- Kerala
- Tamil Nadu

The architecture is designed to support additional Indian states by integrating new climate datasets and retraining the prediction pipeline.

---

# 🎯 Expected Outcomes Achieved

✅ Proof-of-Concept Climate Digital Twin

✅ AI-based Climate Prediction

✅ Flood & Drought Risk Estimation

✅ Interactive Visualization Dashboard

✅ Scenario Simulation (What-if Analysis)

✅ GIS-based Risk Mapping

✅ Live Weather Integration

✅ Data Assimilation

---

# 📈 Future Scope

- Pan-India Digital Twin
- Satellite Data Assimilation
- Explainable AI (SHAP)
- District Boundary GIS Layers
- Temporal Simulation
- Automated Model Retraining
- Cloud Deployment

---

#