import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function color(score) {
  if (score >= 75) return "#dc2626";
  if (score >= 50) return "#d97706";
  if (score >= 30) return "#ca8a04";
  return "#059669";
}

export default function RiskLayerMap({ points = [], region = "Kerala", layer = "flood" }) {
  const center = region === "Tamil Nadu" ? [11.1, 78.6] : [10.3, 76.4];

  return (
    <div className="risk-layer-map">
      <MapContainer center={center} zoom={7} style={{ height: "100%", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {points.map((p, i) => {
          const score =
            layer === "drought"
              ? Number(p.drought_risk_index || p.scenario_drought || 0)
              : Number(p.flood_risk_index || p.scenario_flood || 0);

          return (
            <CircleMarker
              key={i}
              center={[p.lat, p.lon]}
              radius={Math.max(7, score / 8)}
              pathOptions={{
                color: color(score),
                fillColor: color(score),
                fillOpacity: 0.58,
                weight: 2,
              }}
            >
              <Popup>
                <b>{p.region || region}</b>
                <br />
                Lat: {Number(p.lat).toFixed(3)}
                <br />
                Lon: {Number(p.lon).toFixed(3)}
                <hr />
                Flood: {Number(p.flood_risk_index || p.scenario_flood || 0).toFixed(1)}%
                <br />
                Drought: {Number(p.drought_risk_index || p.scenario_drought || 0).toFixed(1)}%
                <br />
                T+1: {Number(p.predicted_t1 || p.scenario_t1 || 0).toFixed(2)} mm
                <br />
                T+3: {Number(p.predicted_t3 || p.scenario_t3 || 0).toFixed(2)} mm
                <br />
                T+7: {Number(p.predicted_t7 || p.scenario_t7 || 0).toFixed(2)} mm
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
}