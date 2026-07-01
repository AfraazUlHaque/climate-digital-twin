import { MdDarkMode, MdLightMode, MdBolt, MdMemory } from "react-icons/md";
import { useTheme } from "../context/ThemeContext.jsx";

export default function Topbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="topbar">
      <div>
        <h1>AI Climate Digital Twin</h1>
        <p>Kerala + Tamil Nadu • Weighted GNN • Live Climate Intelligence</p>
      </div>

      <div className="topbar-actions">
        <div className="status-pill">
          <MdBolt />
          Model Online
        </div>

        <div className="status-pill">
          <MdMemory />
          Graph Loaded
        </div>

        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === "dark" ? <MdLightMode /> : <MdDarkMode />}
        </button>
      </div>
    </header>
  );
}