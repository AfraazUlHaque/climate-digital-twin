export default function KPICard({
  title,
  value,
  unit = "",
  icon,
  accent = "#2563eb",
  hint = ""
}) {
  return (
    <div className="kpi-card" style={{ borderTopColor: accent }}>
      <div className="kpi-top">
        <div className="kpi-icon" style={{ color: accent }}>
          {icon}
        </div>
        <p>{title}</p>
      </div>

      <div className="kpi-value">
        {value ?? "--"}
        <span>{unit}</span>
      </div>

      {hint && <div className="kpi-hint">{hint}</div>}
    </div>
  );
}