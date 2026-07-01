import { useEffect, useState } from "react";
import Panel from "../components/Panel";
import Loader from "../components/Loader";
import RegionSelector from "../components/RegionSelector";
import RiskLayerMap from "../components/RiskLayerMap";
import { apiClient } from "../api/api";

export default function GIS() {
  const [region, setRegion] = useState("Kerala");
  const [layer, setLayer] = useState("flood");
  const [horizon, setHorizon] = useState("t1");
  const [points, setPoints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);

      try {
        const res = await apiClient.mapData(region);
        setPoints(res.data.points || []);
      } catch (err) {
        console.error("GIS load failed:", err);
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
          <h1 className="page-title">GIS Explorer</h1>
          <p className="subtitle">
            Spatial flood and drought risk layer from Weighted GNN grid-cell predictions.
          </p>
        </div>

        <div className="control-cluster">
          <RegionSelector region={region} setRegion={setRegion} />

          <select className="select" value={layer} onChange={(e) => setLayer(e.target.value)}>
            <option value="flood">Flood Layer</option>
            <option value="drought">Drought Layer</option>
          </select>

          <select className="select" value={horizon} onChange={(e) => setHorizon(e.target.value)}>
            <option value="t1">T+1</option>
            <option value="t3">T+3</option>
            <option value="t7">T+7</option>
          </select>
        </div>
      </div>

      <Panel
        title={`${region} ${layer === "flood" ? "Flood" : "Drought"} Risk Map`}
        subtitle={`Interactive GIS layer. Horizon selected: ${horizon.toUpperCase()}`}
      >
        <div className="map-toolbar">
          <b>Layer: {layer === "flood" ? "Flood Risk" : "Drought Risk"}</b>

          <div className="map-legend">
            <span className="legend-safe" /> Low
            <span className="legend-mod" /> Moderate
            <span className="legend-high" /> High
            <span className="legend-extreme" /> Extreme
          </div>
        </div>

        <RiskLayerMap points={points} region={region} layer={layer} />
      </Panel>
    </>
  );
}