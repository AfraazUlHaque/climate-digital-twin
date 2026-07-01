import { useEffect, useState } from "react";
import { MdWaterDrop, MdWarning, MdThermostat, MdCloud } from "react-icons/md";
import RiskLayerMap from "../components/RiskLayerMap";
import { apiClient } from "../api/api";
import Loader from "../components/Loader";
import Panel from "../components/Panel";
import KPICard from "../components/KPICard";
import WeatherCard from "../components/WeatherCard";
import ForecastChart from "../components/ForecastChart";
import RiskGauge from "../components/RiskGauge";
import RegionSelector from "../components/RegionSelector";
import { getDashboard, getForecast, getWeather } from "../api/api";
import AssimilationCard from "../components/AssimilationCard";
import ForecastComparison from "../components/ForecastComparison";
import { getAssimilatedForecast } from "../api/api";
export default function Dashboard() {
  const [region, setRegion] = useState("Kerala");
  const [loading, setLoading] = useState(true);

  const [dashboard, setDashboard] = useState({
    region: "Kerala",
    flood_risk: 0,
    drought_risk: 0,
  });
  const [mapPoints, setMapPoints] = useState([]);
  const [assimilation, setAssimilation] = useState(null);

  const [forecast, setForecast] = useState([]);

  const [weather, setWeather] = useState({
    city: "Kochi",
    temperature: 0,
    humidity: 0,
    wind_speed: 0,
    cloud: 0,
  });

  useEffect(() => {
    async function load() {
      setLoading(true);

      try {
    const [d, f, w, mapRes, assim] = await Promise.all([
  getDashboard(region),
  getForecast(region),
  getWeather(region),
  apiClient.mapData(region),
  getAssimilatedForecast(region),
]);

setDashboard(d || { region, flood_risk: 0, drought_risk: 0 });
setForecast(f || []);
setWeather(w || {});
setMapPoints(mapRes?.data?.points || []);
setAssimilation(assim);
      } catch (err) {
        console.error("Dashboard load failed:", err);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [region]);

  if (loading) return <Loader />;

  return (
    <>
      <div className="hero-row">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="subtitle">
            Live AI climate intelligence powered by Weighted GNN.
          </p>
        </div>

        <RegionSelector region={region} setRegion={setRegion} />
      </div>

      <div className="dashboard-grid">
        <KPICard
          title="Flood Risk"
          value={dashboard?.flood_risk ?? 0}
          unit="%"
          accent="#1e25ec"
          icon={<MdWaterDrop />}
          hint={`${dashboard?.region || region} hydrological risk`}
        />

        <KPICard
          title="Drought Risk"
          value={dashboard?.drought_risk ?? 0}
          unit="%"
          accent="#08b7c1"
          icon={<MdWarning />}
          hint={`${dashboard?.region || region} water stress`}
        />

        <KPICard
          title="Temperature"
          value={weather?.temperature ?? "--"}
          unit="°C"
          accent="#dc2626"
          icon={<MdThermostat />}
          hint={weather?.city || "Live city"}
        />

        <KPICard
          title="Humidity"
          value={weather?.humidity ?? "--"}
          unit="%"
          accent="#059669"
          icon={<MdCloud />}
          hint="Open-Meteo live"
        />
      </div>

      <div className="content-grid">
        <Panel title="AI Forecast" subtitle={`Weighted GNN rainfall trend for ${region}`}>
          <ForecastChart data={forecast} />
        </Panel>

        <Panel title="Live Weather" subtitle={`Current atmospheric conditions for ${weather?.city}`}>
          <WeatherCard weather={weather} />
        </Panel>
      </div>

      <Panel
  title="Live Spatial Risk Layer"
  subtitle={`Model-generated grid-cell risk map for ${region}`}
>
  <div className="dashboard-map-wrap">
    <RiskLayerMap points={mapPoints} region={region} layer="flood" />
  </div>
</Panel>

<div className="content-grid">
  <Panel title="Assimilated Forecast" subtitle="Model prediction corrected with live weather observations">
    <ForecastComparison data={assimilation} />
  </Panel>

  <Panel title="Assimilation Engine" subtitle="Live observation signal applied to Weighted GNN forecast">
    <AssimilationCard data={assimilation} />
  </Panel>
</div>

      <div className="risk-grid">
        <RiskGauge
          title="Flood Probability"
          value={dashboard?.flood_risk ?? 0}
          color="#2563eb"
        />

        <RiskGauge
          title="Drought Probability"
          value={dashboard?.drought_risk ?? 0}
          color="#d97706"
        />
      </div>
    </>
  );
}