import React, { useEffect, useState } from 'react';
import { getLiveWeather, getForecast } from '../api/api';

function Home() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardDefault() {
      try {
        const weatherRes = await getLiveWeather('Region-1');
        const forecastRes = await getForecast('Region-1', '2026-06-27');
        setData({ weather: weatherRes.data, forecast: forecastRes.data });
      } catch (err) {
        console.error("Failed loading backend pipeline parameters", err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardDefault();
  }, []);

  if (loading) return <div>Synchronizing Core Digital Twin State Matrix...</div>;

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem' }}>AI Climate Digital Twin Framework Dashboard</h2>
      
      <div className="dashboard-grid">
        <div className="metric-card">
          <div className="metric-header">Active Micro-Climate Target</div>
          <div className="metric-value">{data?.weather?.region || "Region-1"}</div>
        </div>
        <div className="metric-card">
          <div className="metric-header">Ambient Temperature Surface</div>
          <div className="metric-value" style={{ color: 'var(--accent-cyan)' }}>{data?.weather?.temperature}°C</div>
        </div>
        <div className="metric-card">
          <div className="metric-header">GNN Next-Day Precipitation Forecast</div>
          <div className="metric-value" style={{ color: 'var(--accent-blue)' }}>{data?.forecast?.forecast_t1} mm</div>
        </div>
      </div>

      <div className="chart-wrapper">
        <h3>Architecture System Configuration Matrix Overview</h3>
        <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem', lineHeight: '1.6' }}>
          This infrastructure utilizes an un-batched **Graph Neural Network (GNN)** cross-referenced continuously with spatio-temporal layers. Direct message-passing graph networks construct relationships across localized edge sensors to synthesize real-time downstream predictive hydro-met dynamics.
        </p>
      </div>
    </div>
  );
}

export default Home;