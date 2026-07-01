import { useState } from "react";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

import Panel from "../components/Panel";
import RiskGauge from "../components/RiskGauge";
import RegionSelector from "../components/RegionSelector";
import ScenarioLineChart from "../components/ScenarioLineChart";
import ScenarioHeatmap from "../components/ScenarioHeatmap";
import { runAdvancedWhatIf } from "../api/api";

function riskColor(score) {
  if (score >= 75) return "#dc2626";
  if (score >= 50) return "#d97706";
  if (score >= 30) return "#ca8a04";
  return "#059669";
}

function deltaColor(value) {
  if (value > 15) return "#dc2626";
  if (value > 5) return "#f97316";
  if (value > 0) return "#facc15";
  if (value > -5) return "#e5e7eb";
  return "#2563eb";
}

function avg(points, key) {
  if (!points.length) return 0;
  return points.reduce((s, p) => s + Number(p[key] || 0), 0) / points.length;
}

export default function WhatIf() {
  const [region, setRegion] = useState("Kerala");
  const [rain, setRain] = useState(0);
  const [temp, setTemp] = useState(0);
  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  async function simulate() {
    setLoading(true);

    try {
      const data = await runAdvancedWhatIf({
        region,
        rainfall_change: rain,
        temperature_change: temp,
      });

      setResult(data);
    } catch (err) {
      console.error("What-if failed:", err);
      alert(err?.response?.data?.detail || err.message || "Simulation failed");
    } finally {
      setLoading(false);
    }
  }

  const points = result?.points || [];
  const summary = result?.summary || {};

  const center = region === "Tamil Nadu" ? [11.1, 78.6] : [10.3, 76.4];

  const lineData = [
    {
      label: "T+1",
      baseline: Number(summary.baseline_t1 || 0),
      scenario: Number(summary.scenario_t1 || 0),
    },
    {
      label: "T+3",
      baseline: Number(summary.baseline_t3 || 0),
      scenario: Number(summary.scenario_t3 || 0),
    },
    {
      label: "T+7",
      baseline: Number(summary.baseline_t7 || 0),
      scenario: Number(summary.scenario_t7 || 0),
    },
  ];

  const topRisk = [...points]
    .sort((a, b) => Number(b.scenario_flood || 0) - Number(a.scenario_flood || 0))
    .slice(0, 6);

  const aiAdvice = (() => {
    const flood = Number(summary.scenario_flood || 0);
    const drought = Number(summary.scenario_drought || 0);

    if (flood >= 70) {
      return "High flood risk detected. Prioritize low-lying zones, reservoir monitoring, and emergency alert readiness.";
    }

    if (drought >= 70) {
      return "High drought stress detected. Recommend irrigation support, reservoir conservation, and crop stress monitoring.";
    }

    if (rain > 40) {
      return "Rainfall scenario shows increased wet conditions. Continue monitoring flood-prone grids and drainage capacity.";
    }

    if (temp > 3) {
      return "Temperature stress is rising. Monitor drought-sensitive regions and agricultural water demand.";
    }

    return "Scenario remains within moderate range. Continue real-time monitoring and compare with live weather assimilation.";
  })();

  return (
    <>
      <div className="hero-row">
        <div>
          <h1 className="page-title">What-if Simulator</h1>
          <p className="subtitle">
            Trained Weighted GNN counterfactual simulation with spatial risk layers.
          </p>
        </div>

        <RegionSelector region={region} setRegion={setRegion} />
      </div>

      <Panel
        title="Scenario Controls"
        subtitle="Modify rainfall and temperature, then rerun the trained model."
      >
        <div className="whatif-control-grid">
          <div className="scenario-card">
            <label>Rainfall Change</label>
            <input
              type="range"
              min="-100"
              max="100"
              value={rain}
              onChange={(e) => setRain(Number(e.target.value))}
            />
            <h2>{rain > 0 ? `+${rain}` : rain}%</h2>
            <p>Applied to rainfall-sensitive model features.</p>
          </div>

          <div className="scenario-card">
            <label>Temperature Change</label>
            <input
              type="range"
              min="-7"
              max="7"
              step="0.5"
              value={temp}
              onChange={(e) => setTemp(Number(e.target.value))}
            />
            <h2>{temp > 0 ? `+${temp}` : temp}°C</h2>
            <p>Applied to temperature-sensitive model features.</p>
          </div>

          <button
            className="primary-btn whatif-run-btn"
            onClick={simulate}
            disabled={loading}
          >
            {loading ? "Running Model..." : "Run AI Simulation"}
          </button>
        </div>
      </Panel>

      {result && (
        <>
          <div className="scenario-summary-grid">
            <div className="scenario-summary-card">
              <p>Baseline Flood</p>
              <h2>{Number(summary.baseline_flood || 0).toFixed(1)}%</h2>
            </div>

            <div className="scenario-summary-card">
              <p>Scenario Flood</p>
              <h2>{Number(summary.scenario_flood || 0).toFixed(1)}%</h2>
            </div>

            <div className="scenario-summary-card">
              <p>Rainfall Delta</p>
              <h2>{Number(summary.delta_rainfall || 0).toFixed(2)} mm</h2>
            </div>

            <div className="scenario-summary-card">
              <p>Flood Delta</p>
              <h2>{Number(summary.delta_flood || 0).toFixed(1)}%</h2>
            </div>
          </div>

          <div className="risk-grid">
            <RiskGauge
              title="Scenario Flood Risk"
              value={Number(summary.scenario_flood || 0)}
              color="#2563eb"
            />

            <RiskGauge
              title="Scenario Drought Risk"
              value={Number(summary.scenario_drought || 0)}
              color="#d97706"
            />
          </div>

          <Panel title="AI Scenario Recommendation" subtitle="Generated from model risk deltas.">
            <div className="ai-recommendation-box">
              <h3>Recommended Action</h3>
              <p>{aiAdvice}</p>
            </div>
          </Panel>

          <div className="content-grid">
            <Panel
              title="Baseline vs Scenario Rainfall"
              subtitle="Model prediction comparison across forecast horizons."
            >
              <ScenarioLineChart data={lineData} />
            </Panel>

            <Panel
              title="Rainfall Difference Heatmap"
              subtitle="Grid-cell rainfall delta from trained model output."
            >
              <ScenarioHeatmap
                points={points}
                type="rainfall"
              />
            </Panel>
          </div>

          <div className="content-grid">
            <Panel
              title="Flood Risk Difference Heatmap"
              subtitle="Spatial flood-risk delta after scenario simulation."
            >
              <ScenarioHeatmap
                points={points}

                type="risk"
              />
            </Panel>

            <Panel title="Top Affected Grid Cells" subtitle="Highest scenario flood risk cells.">
              <table className="forecast-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Lat</th>
                    <th>Lon</th>
                    <th>Flood</th>
                    <th>Δ Flood</th>
                  </tr>
                </thead>
                <tbody>
                  {topRisk.map((p, i) => (
                    <tr key={i}>
                      <td>{i + 1}</td>
                      <td>{Number(p.lat).toFixed(2)}</td>
                      <td>{Number(p.lon).toFixed(2)}</td>
                      <td>{Number(p.scenario_flood).toFixed(1)}%</td>
                      <td>{Number(p.delta_flood).toFixed(1)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Panel>
          </div>

          <Panel
  title="Interactive GIS Scenario Heatmap"
  subtitle="Actual latitude-longitude based flood and rainfall risk layer from trained model outputs."
>
  <div className="map-toolbar">
    <div>
      <b>Layer:</b> Flood Risk
    </div>
    <div className="map-legend">
      <span className="legend-safe"></span> Low
      <span className="legend-mod"></span> Moderate
      <span className="legend-high"></span> High
      <span className="legend-extreme"></span> Extreme
    </div>
  </div>

  <div className="whatif-map big-risk-map">
    <MapContainer
      center={center}
      zoom={7}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {points.map((p, i) => {
        const flood = Number(p.scenario_flood || 0);
        const drought = Number(p.scenario_drought || 0);
        const deltaFlood = Number(p.delta_flood || 0);
        const deltaRain = Number(p.delta_rainfall || 0);
        const risk = Math.max(flood, drought);

        return (
          <CircleMarker
            key={i}
            center={[p.lat, p.lon]}
            radius={Math.max(8, risk / 7)}
            pathOptions={{
              color: riskColor(risk),
              fillColor: riskColor(risk),
              fillOpacity: 0.55,
              weight: 2,
            }}
          >
            <Popup>
              <div style={{ minWidth: 220 }}>
                <b>{region} Scenario Grid Cell</b>
                <br />
                Lat: {Number(p.lat).toFixed(3)}
                <br />
                Lon: {Number(p.lon).toFixed(3)}
                <hr />
                <b>Rainfall</b>
                <br />
                Baseline T+7: {Number(p.baseline_t7).toFixed(2)} mm
                <br />
                Scenario T+7: {Number(p.scenario_t7).toFixed(2)} mm
                <br />
                Δ Rainfall: {deltaRain.toFixed(2)} mm
                <hr />
                <b>Flood Risk</b>
                <br />
                Baseline: {Number(p.baseline_flood).toFixed(1)}%
                <br />
                Scenario: {flood.toFixed(1)}%
                <br />
                Δ Flood: {deltaFlood.toFixed(1)}%
                <hr />
                <b>Drought Risk</b>
                <br />
                Baseline: {Number(p.baseline_drought).toFixed(1)}%
                <br />
                Scenario: {drought.toFixed(1)}%
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  </div>
</Panel>
        </>
      )}
    </>
  );
}