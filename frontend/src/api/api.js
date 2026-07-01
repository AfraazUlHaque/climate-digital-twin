import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 120000,
});

export default api;

export function regionToCity(region) {
  const map = {
    Kerala: "Kochi",
    "Tamil Nadu": "Chennai",
    Kochi: "Kochi",
    Chennai: "Chennai",
    Kozhikode: "Kozhikode",
    Thiruvananthapuram: "Thiruvananthapuram",
    Madurai: "Madurai",
    Coimbatore: "Coimbatore",
  };

  return map[region] || region || "Kochi";
}

export async function getRegions() {
  const res = await api.get("/regions");
  return res.data.regions || ["Kerala", "Tamil Nadu"];
}

export async function getDashboard(region = "Kerala") {
  const res = await api.get("/forecast", { params: { region } });
  const d = res.data;

  return {
    region: d.region,
    flood_risk: Number(d.risk?.flood?.score || 0).toFixed(1),
    drought_risk: Number(d.risk?.drought?.score || 0).toFixed(1),
    forecast: d.forecast,
    risk: d.risk,
  };
}

export async function getForecast(region = "Kerala") {
  const res = await api.get("/forecast/history", { params: { region } });

  return (res.data.history || []).map((x) => ({
    time: x.date,
    predicted_t1: Number(x.predicted_t1 || 0),
    predicted_t3: Number(x.predicted_t3 || 0),
    predicted_t7: Number(x.predicted_t7 || 0),
  }));
}

export async function getWeather(cityOrRegion = "Kochi") {
  const safeCity = regionToCity(cityOrRegion);

  const res = await api.get("/live-weather", {
    params: { city: safeCity },
  });

  const w = res.data;
  const current = w.current || {};

  return {
    city: w.city || safeCity,
    temperature: Number(current.temperature ?? 0).toFixed(1),
    feels_like: Number(current.temperature ?? 0).toFixed(1),
    humidity: Number(current.humidity ?? 0).toFixed(0),
    wind_speed: Number(current.wind_speed ?? 0).toFixed(1),
    cloud: Number(current.precipitation ?? 0).toFixed(1),
    daily: w.daily || {},
  };
}

export async function getAnalytics() {
  const res = await api.get("/metrics");
  const models = res.data.models || [];

  return models.map((m) => ({
    metric: m.model,
    value: Number(m.r2 || 0),
    mae: Number(m.mae || 0),
    rmse: Number(m.rmse || 0),
  }));
}

export async function runSimulation(payload) {
  const res = await api.post("/what-if", {
    region: payload.region || "Kerala",
    horizon: payload.horizon || "t1",
    rainfall_change: payload.rainfall_change ?? payload.rainfall_delta ?? 0,
    temperature_change: payload.temperature_change ?? payload.temperature_delta ?? 0,
  });

  return {
    flood_risk: Number(res.data.flood?.score || 0).toFixed(1),
    drought_risk: Number(res.data.drought?.score || 0).toFixed(1),
    raw: res.data,
  };
}

export async function runSimulationMap(payload) {
  const res = await api.get("/map-data", {
    params: {
      region: payload.region || "Kerala",
    },
  });

  return {
    region: res.data.region,
    scenario: {
      rainfall_change: payload.rainfall_change ?? 0,
      temperature_change: payload.temperature_change ?? 0,
    },
    points: res.data.points || [],
  };
}
export async function runAdvancedWhatIf(payload) {
  const res = await api.post("/what-if-grid", {
    region: payload.region || "Kerala",
    rainfall_change: payload.rainfall_change ?? 0,
    temperature_change: payload.temperature_change ?? 0,
  });

  return res.data;
}

export const apiClient = {
  regions: () => api.get("/regions"),
  dates: (region) => api.get("/dates", { params: { region } }),
  forecast: (region, date) => api.get("/forecast", { params: { region, date } }),
  history: (region) => api.get("/forecast/history", { params: { region } }),
  mapData: (region, date) => api.get("/map-data", { params: { region, date } }),
  flood: (region, date) => api.get("/flood-risk", { params: { region, date } }),
  drought: (region, date) => api.get("/drought-risk", { params: { region, date } }),
  weather: (cityOrRegion) =>
    api.get("/live-weather", { params: { city: regionToCity(cityOrRegion) } }),
  metrics: () => api.get("/metrics"),
  whatIf: (payload) => api.post("/what-if", payload),
};
export async function getAssimilatedForecast(region = "Kerala") {
  const res = await api.get("/assimilated-forecast", {
    params: { region },
  });

  const d = res.data;
  

  return {
    region: d.region,
    model_forecast: d.model_forecast,
    assimilated_forecast: d.assimilated_forecast,
    signal: d.live_observation_signal,
    flood_risk: Number(d.risk?.flood?.score || 0).toFixed(1),
    drought_risk: Number(d.risk?.drought?.score || 0).toFixed(1),
    raw: d,
  };
}
export async function getAssimilationHistory() {
    const res = await api.get("/assimilation-history");
    return res.data.history;
}