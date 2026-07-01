# 🌍 ZENORA - AI Climate Digital Twin

> **AI-Powered Digital Twin of India's Climate using India's National Data**

ZENORA is an AI-powered Climate Digital Twin developed for **ISRO BAH 2026**. The platform combines **Weighted Graph Neural Networks (Weighted GNN)**, **GIS-based spatial intelligence**, and **live weather data assimilation** to create a virtual representation of regional climate conditions. It enables intelligent climate forecasting, flood and drought risk assessment, interactive visualization, and scenario-based climate simulations.

The current Proof-of-Concept focuses on **Kerala** and **Tamil Nadu**, while the modular GIS framework allows seamless expansion to all Indian states.

---

# ✨ Key Features

- 🌦 AI-powered Climate Forecasting
- 🌍 Climate Digital Twin Visualization
- 🛰 Historical Climate Data Integration
- ☁ Live Weather Data Assimilation
- 🗺 GIS-based Spatial Intelligence
- 🌊 Flood Risk Prediction
- 🌾 Drought Risk Assessment
- 🤖 Weighted Graph Neural Network (Weighted GNN)
- 📊 Interactive Dashboard
- 🔍 Historical Climate Analytics
- 🎯 What-if Scenario Simulator
- ⚠ Early Decision Support System
- 🇮🇳 Scalable to Pan-India Deployment

---

# 🏗 System Architecture

```
Historical Climate Data
          │
          ▼
 Data Preprocessing
(Normalization • GIS Masking • Feature Engineering)
          │
          ▼
 Weighted Graph Neural Network
          │
          ▼
 Live Weather Data Assimilation
          │
          ▼
 Climate Digital Twin
          │
          ▼
 Dashboard • Forecast • Flood Risk • Drought Risk
          │
          ▼
 What-if Scenario Simulation
```

---

# 🧠 AI Model

## Final Model

- Weighted Graph Neural Network (Weighted GNN)

## Baseline Model

- ExtraTrees Regressor

## Experimental Model

- Hybrid LSTM + GNN

After evaluating multiple approaches, **Weighted GNN** was selected because it provided the best balance of spatial learning capability, forecasting accuracy, scalability, and real-time inference performance.

---

# 🛰 Data Sources

- IMD Historical Climate Data
- Open-Meteo Weather API
- GIS Shapefiles
- Terrain & Spatial Data

---

# 💻 Tech Stack

### AI & Machine Learning

- PyTorch
- Scikit-learn
- NumPy
- Pandas

### GIS

- GeoPandas
- Shapely
- Leaflet
- GIS Masking

### Backend

- Python
- FastAPI
- Uvicorn

### Frontend

- React.js
- Vite
- Axios

### Visualization

- Matplotlib
- Recharts
- Leaflet Maps

---

# 📂 Project Structure

```
backend/
frontend/
eda/
pipeline/
README.md
.gitignore
```

---

# 🚀 Future Scope

- Expansion to all Indian states
- Multi-hazard forecasting
- Cyclone & Heatwave Prediction
- Satellite Image Assimilation
- ISRO Data Integration
- Mobile Application
- Real-time Alert System
- Decision Support for Government Agencies

---

# 👥 Team

### Team Name

**ZENORA**

### Problem Statement

**AI-Powered Digital Twin of India's Climate using India's National Data**

### Team Leader

**Afraaz Ul Haque**

### Team Members

- Naira Karim
- Nasir Yousuf
- Hamza Ansari

---

# 🏆 Developed For

**ISRO BAH 2026**

Building an intelligent Climate Digital Twin for regional climate forecasting, disaster preparedness, and data-driven decision support.

---

## ⭐ If you found this project interesting, don't forget to Star the repository!
