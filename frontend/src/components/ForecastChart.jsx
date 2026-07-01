import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

export default function ForecastChart({ data = [], dataKey = "predicted_t1" }) {
  const chartData = data.length ? data : [];

  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height={340}>
        <LineChart data={chartData}>
          <CartesianGrid stroke="#e5e7eb" strokeDasharray="4 4" />

          <XAxis
            dataKey="time"
            tick={{ fill: "#64748b", fontSize: 12 }}
            minTickGap={28}
          />

          <YAxis
            tick={{ fill: "#64748b", fontSize: 12 }}
            label={{
              value: "Rainfall (mm)",
              angle: -90,
              position: "insideLeft",
              fill: "#64748b",
            }}
          />

          <Tooltip
            formatter={(value) => [`${Number(value).toFixed(2)} mm`, "Prediction"]}
            labelFormatter={(label) => `Date: ${label}`}
            contentStyle={{
              background: "#ffffff",
              border: "1px solid #e5e7eb",
              borderRadius: 10,
              color: "#111827",
            }}
          />

          <Line
            type="monotone"
            dataKey={dataKey}
            stroke="#2563eb"
            strokeWidth={3}
            dot={false}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}