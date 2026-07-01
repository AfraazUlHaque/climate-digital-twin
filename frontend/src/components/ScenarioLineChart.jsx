import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

export default function ScenarioLineChart({ data = [], metric = "rainfall" }) {
  const title = metric === "rainfall" ? "Rainfall (mm)" : "Risk (%)";

  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height={330}>
        <LineChart data={data}>
          <CartesianGrid stroke="#e5e7eb" strokeDasharray="4 4" />
          <XAxis dataKey="label" tick={{ fill: "#64748b", fontSize: 12 }} />
          <YAxis tick={{ fill: "#64748b", fontSize: 12 }} />
          <Tooltip />
          <Legend />
          <Line
            name={`Baseline ${title}`}
            type="monotone"
            dataKey="baseline"
            stroke="#64748b"
            strokeWidth={3}
            dot={{ r: 4 }}
          />
          <Line
            name={`Scenario ${title}`}
            type="monotone"
            dataKey="scenario"
            stroke="#2563eb"
            strokeWidth={3}
            dot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}