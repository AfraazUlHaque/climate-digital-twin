import EDAImageCard from "../components/EDAImageCard";
import Panel from "../components/Panel";
import KPICard from "../components/KPICard";
import {
  MdWaterDrop,
  MdThermostat,
  MdAnalytics,
  MdTableChart,
} from "react-icons/md";

const EDA_BASE = "http://127.0.0.1:8000/eda";

const edaImages = [
  {
    title: "Average Monthly Rainfall",
    subtitle: "Historical monthly precipitation behaviour",
    image: `${EDA_BASE}/monthly_rainfall.png`,
  },
  {
    title: "Daily Rainfall Trend",
    subtitle: "Day-level rainfall variation",
    image: `${EDA_BASE}/daily_rainfall.png`,
  },
  {
    title: "Average Monthly Tmax",
    subtitle: "Monthly maximum temperature pattern",
    image: `${EDA_BASE}/monthly_tmax.png`,
  },
  {
    title: "Daily Tmax Trend",
    subtitle: "Daily maximum temperature variation",
    image: `${EDA_BASE}/daily_tmax.png`,
  },
  {
    title: "Rainfall Distribution",
    subtitle: "Distribution of rainfall intensity",
    image: `${EDA_BASE}/rainfall_distribution.png`,
  },
  {
    title: "Tmax Distribution",
    subtitle: "Maximum temperature distribution",
    image: `${EDA_BASE}/tmax_distribution.png`,
  },
  {
    title: "Tmin Distribution",
    subtitle: "Minimum temperature distribution",
    image: `${EDA_BASE}/tmin_distribution.png`,
  },
  {
    title: "Correlation Matrix",
    subtitle: "Feature relationships used for climate intelligence",
    image: `${EDA_BASE}/correlation.png`,
  },
];

export default function Analytics() {
  return (
    <>
      <div className="hero-row">
        <div>
          <h1 className="page-title">Climate Analytics</h1>
          <p className="subtitle">
            Exploratory data analysis outputs used to understand rainfall,
            temperature and feature relationships.
          </p>
        </div>
      </div>

      <div className="dashboard-grid">
        <KPICard
          title="EDA Visuals"
          value="8"
          icon={<MdAnalytics />}
          accent="#2563eb"
          hint="Generated plots"
        />

        <KPICard
          title="Rainfall Studies"
          value="3"
          icon={<MdWaterDrop />}
          accent="#059669"
          hint="Trend + distribution"
        />

        <KPICard
          title="Temperature Studies"
          value="4"
          icon={<MdThermostat />}
          accent="#dc2626"
          hint="Tmax/Tmin analysis"
        />

        <KPICard
          title="Region Summary"
          value="CSV"
          icon={<MdTableChart />}
          accent="#7c3aed"
          hint="Available in outputs"
        />
      </div>

      <Panel
        title="EDA Insights"
        subtitle="These plots help explain model behaviour before prediction and simulation."
      >
        <div className="eda-insight-grid">
          <div className="eda-insight">
            <h3>Rainfall Seasonality</h3>
            <p>
              Monthly rainfall trend helps identify wet-season behaviour and
              flood-sensitive periods.
            </p>
          </div>

          <div className="eda-insight">
            <h3>Temperature Stress</h3>
            <p>
              Tmax and Tmin trends support drought and heat-stress interpretation.
            </p>
          </div>

          <div className="eda-insight">
            <h3>Feature Relationship</h3>
            <p>
              Correlation analysis shows how climate variables interact before
              model inference.
            </p>
          </div>
        </div>
      </Panel>

      <div className="eda-grid">
        {edaImages.map((item) => (
          <EDAImageCard key={item.title} {...item} />
        ))}
      </div>
    </>
  );
}