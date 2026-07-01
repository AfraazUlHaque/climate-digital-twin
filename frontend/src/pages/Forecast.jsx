import { useEffect, useState } from "react";
import Panel from "../components/Panel";
import ForecastChart from "../components/ForecastChart";
import Loader from "../components/Loader";
import RegionSelector from "../components/RegionSelector";
import { getForecast } from "../api/api";

export default function Forecast() {
  const [region, setRegion] = useState("Kerala");
  const [horizon, setHorizon] = useState("predicted_t1");
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await getForecast(region);
        setForecast(data);
      } catch (err) {
        console.error("Forecast load failed:", err);
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
          <h1 className="page-title">Forecast Engine</h1>
          <p className="subtitle">
            Region-wise Weighted GNN rainfall prediction.
          </p>
        </div>

        <div className="control-cluster">
          <RegionSelector region={region} setRegion={setRegion} />

          <select
            className="select"
            value={horizon}
            onChange={(e) => setHorizon(e.target.value)}
          >
            <option value="predicted_t1">T+1</option>
            <option value="predicted_t3">T+3</option>
            <option value="predicted_t7">T+7</option>
          </select>
        </div>
      </div>

      <Panel
        title={`${region} Forecast Curve`}
        subtitle={`Showing ${horizon.replace("predicted_", "").toUpperCase()} rainfall prediction`}
      >
        <ForecastChart data={forecast} dataKey={horizon} />
      </Panel>
    </>
  );
}