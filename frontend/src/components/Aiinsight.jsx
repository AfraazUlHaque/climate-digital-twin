import { MdAutoAwesome } from "react-icons/md";

export default function AIInsight({ summary }) {
  const forecast = summary?.forecast || {};
  const flood = summary?.risk?.flood || {};
  const drought = summary?.risk?.drought || {};

  const t3 = Number(forecast.t3 || 0).toFixed(1);
  const floodScore = Number(flood.score || 0).toFixed(1);
  const droughtScore = Number(drought.score || 0).toFixed(1);

  return (
    <div className="ai-insight">
      <div className="ai-title">
        <MdAutoAwesome />
        <span>AI Insight</span>
      </div>

      <p>
        The Weighted GNN predicts an average <b>{t3} mm</b> rainfall over the T+3 horizon.
        Flood risk is currently <b>{flood.level || "Unknown"}</b> at <b>{floodScore}%</b>,
        while drought stress is <b>{drought.level || "Unknown"}</b> at <b>{droughtScore}%</b>.
      </p>

      <div className="ai-actions">
        <span>Model: Weighted GNN</span>
        <span>Mode: MVP Live</span>
      </div>
    </div>
  );
}