export default function AssimilationCard({ data }) {
  if (!data) return null;

  const model = data.model_forecast || {};
  const assim = data.assimilated_forecast || {};
  const signal = data.signal || {};

  return (
    <div className="assim-card">
      <div className="assim-head">
        <div>
          <p className="label">DATA ASSIMILATION</p>
          <h2>Model + Live Weather Correction</h2>
        </div>

        <div className="assim-status">Active</div>
      </div>

      <div className="assim-grid">
        <div>
          <p>Model T+1</p>
          <h3>{Number(model.t1 || 0).toFixed(2)} mm</h3>
        </div>

        <div>
          <p>Assimilated T+1</p>
          <h3>{Number(assim.t1 || 0).toFixed(2)} mm</h3>
        </div>

        <div>
          <p>Live Rain Signal</p>
          <h3>{Number(signal.rainfall_signal || 0).toFixed(2)}</h3>
        </div>

        <div>
          <p>Observation</p>
          <h3>{Number(signal.precipitation || 0).toFixed(2)} mm</h3>
        </div>
      </div>

      <div className="assim-note">
        The trained Weighted GNN forecast is corrected using live weather observations.
      </div>
    </div>
  );
}