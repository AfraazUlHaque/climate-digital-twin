import { NavLink } from "react-router-dom";
import {
  MdDashboard,
  MdTimeline,
  MdWaterDrop,
  MdCloud,
  MdMap,
  MdSunny,
  MdScience,
  MdAnalytics
} from "react-icons/md";

const links = [
  { label: "DashBoard", path: "/", icon: <MdDashboard /> },
  { label: "Forecast", path: "/forecast", icon: <MdTimeline /> },
  { label: "Flood Intel", path: "/flood", icon: <MdWaterDrop /> },
  { label: "Drought Intel", path: "/drought", icon: <MdCloud /> },
  { label: "GIS Explorer", path: "/gis", icon: <MdMap /> },
  { label: "Live Weather", path: "/weather", icon: <MdSunny /> },
  { label: "What-if", path: "/what-if", icon: <MdScience /> },
  { label: "Analytics", path: "/analytics", icon: <MdAnalytics /> }
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-orb">🌍</div>

        <div>
          <h2>ClimateDT</h2>
          <p>AI Digital Twin</p>
        </div>
      </div>

      <nav className="nav-menu">
        {links.map((item) => (
          <NavLink key={item.path} to={item.path} className="nav-link">
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span className="pulse-dot" />
        Weighted GNN Online
      </div>
    </aside>
  );
}