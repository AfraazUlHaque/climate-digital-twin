import React, { useEffect, useState } from 'react';
import { getMetrics } from '../api/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function ModelPerformance() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    getMetrics().then(res => setMetrics(res.data)).catch(() => {});
  }, []);

  const dataTransform = metrics ? Object.keys(metrics).map(key => ({
    name: key,
    MAE: metrics[key].MAE,
    RMSE: metrics[key].RMSE,
    R2: metrics[key].R2
  })) : [];

  return (
    <div>
      <h2>Machine Learning Benchmarking Configuration Core</h2>
      <div className="chart-wrapper">
        <h3>Model Comparison Target Tracking Matrix</h3>
        <div style={{ width: '100%', height: 400, marginTop: '1rem' }}>
          <ResponsiveContainer>
            <BarChart data={dataTransform}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="name" stroke="var(--text-muted)" />
              <YAxis stroke="var(--text-muted)" />
              <Tooltip contentStyle={{ backgroundColor: 'var(--bg-surface)' }} />
              <Legend />
              <Bar dataKey="MAE" fill="var(--accent-cyan)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="RMSE" fill="var(--accent-blue)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default ModelPerformance;