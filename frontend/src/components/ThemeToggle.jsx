import { MdDarkMode, MdLightMode } from "react-icons/md";
import { useTheme } from "../context/ThemeContext";

export default function ThemeToggle() {
  const context = useTheme();

  if (!context) {
    return null;
  }

  const { theme, toggleTheme } = context;

  return (
    <button className="theme-btn" onClick={toggleTheme}>
      {theme === "dark" ? <MdLightMode size={22} /> : <MdDarkMode size={22} />}
    </button>
  );
}