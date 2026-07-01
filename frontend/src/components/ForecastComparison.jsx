import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

export default function ForecastComparison({ data }) {
  if (!data) return null;

  const model = data.model_forecast || {};
  const assim = data.assimilated_forecast || {};

  const chartData = [
    {
      horizon: "T+1",
      Model: Number(model.t1 || 0),
      Assimilated: Number(assim.t1 || 0),
    },
    {
      horizon: "T+3",
      Model: Number(model.t3 || 0),
      Assimilated: Number(assim.t3 || 0),
    },
    {
      horizon: "T+7",
      Model: Number(model.t7 || 0),
      Assimilated: Number(assim.t7 || 0),
    },
  ];

  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={chartData}>
          <CartesianGrid stroke="#e5e7eb" strokeDasharray="4 4" />
          <XAxis dataKey="horizon" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="Model" fill="#64748b" />
          <Bar dataKey="Assimilated" fill="#2563eb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}