import {
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
  ResponsiveContainer
} from "recharts";

function getLevel(score) {
  if (score >= 70) return "High";
  if (score >= 40) return "Medium";
  return "Low";
}

export default function RiskGauge({ title, value = 0, color = "#38bdf8" }) {
  const score = Number(value || 0);
  const data = [{ name: title, value: score }];

  return (
    <div className="risk-gauge">
      <div className="risk-gauge-chart">
        <ResponsiveContainer width="100%" height={230}>
          <RadialBarChart
            cx="50%"
            cy="50%"
            innerRadius="70%"
            outerRadius="95%"
            barSize={18}
            data={data}
            startAngle={90}
            endAngle={-270}
          >
            <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
            <RadialBar
              background={{ fill: "rgba(148,163,184,.18)" }}
              dataKey="value"
              fill={color}
              cornerRadius={20}
            />
          </RadialBarChart>
        </ResponsiveContainer>

        <div className="risk-gauge-center">
          <h2>{score.toFixed(1)}%</h2>
          <p>{getLevel(score)}</p>
        </div>
      </div>

      <h3>{title}</h3>
    </div>
  );
}