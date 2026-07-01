function getColor(v, min, max) {
  if (max === min) return "#94a3b8";
  const r = (v - min) / (max - min);

  if (r < 0.2) return "#2563eb";
  if (r < 0.4) return "#38bdf8";
  if (r < 0.6) return "#facc15";
  if (r < 0.8) return "#f97316";
  return "#dc2626";
}

export default function ScenarioHeatmap({ points = [], type = "rainfall" }) {
  const valid = points
    .filter((p) => p.lat !== undefined && p.lon !== undefined)
    .slice(0, 250);

  const values = valid.map((p) =>
    type === "rainfall"
      ? Number(p.delta_rainfall || 0)
      : Number(p.delta_risk || p.delta_flood || 0)
  );

  const lats = valid.map((p) => Number(p.lat));
  const lons = valid.map((p) => Number(p.lon));

  const minLat = Math.min(...lats);
  const maxLat = Math.max(...lats);
  const minLon = Math.min(...lons);
  const maxLon = Math.max(...lons);
  const minVal = Math.min(...values);
  const maxVal = Math.max(...values);

  if (!valid.length) {
    return <div className="empty-heatmap">No spatial data available</div>;
  }

  return (
    <div className="spatial-heatmap-card">
      <div className="spatial-legend">
        <span>Lower</span>
        <div className="spatial-legend-bar" />
        <span>Higher</span>
      </div>

      <svg className="spatial-heatmap" viewBox="0 0 100 70">
        <rect x="0" y="0" width="100" height="70" rx="4" className="map-bg" />

        {valid.map((p, i) => {
          const lat = Number(p.lat);
          const lon = Number(p.lon);

          const x = ((lon - minLon) / (maxLon - minLon || 1)) * 88 + 6;
          const y = 64 - ((lat - minLat) / (maxLat - minLat || 1)) * 58;

          const value =
            type === "rainfall"
              ? Number(p.delta_rainfall || 0)
              : Number(p.delta_risk || p.delta_flood || 0);

          return (
            <circle
              key={i}
              cx={x}
              cy={y}
              r="2.2"
              fill={getColor(value, minVal, maxVal)}
              opacity="0.9"
            >
              <title>
                Lat: {lat.toFixed(2)}, Lon: {lon.toFixed(2)}, Δ:{" "}
                {value.toFixed(2)}
              </title>
            </circle>
          );
        })}
      </svg>
    </div>
  );
}