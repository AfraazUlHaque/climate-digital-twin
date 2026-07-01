import { useEffect, useState } from "react";
import { MdAir, MdCloud, MdThermostat, MdWaterDrop } from "react-icons/md";

import Loader from "../components/Loader";
import Panel from "../components/Panel";
import { getWeather } from "../api/api";

export default function Weather() {
  const [city, setCity] = useState("Kochi");
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const weatherData = await getWeather(city);
        setWeather(weatherData);
      } catch (err) {
        console.error("Weather load failed:", err);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [city]);

  if (loading) return <Loader />;

  const items = [
    { label: "Temperature", value: `${weather?.temperature ?? "--"}°C`, icon: <MdThermostat />, color: "#dc2626" },
    { label: "Humidity", value: `${weather?.humidity ?? "--"}%`, icon: <MdWaterDrop />, color: "#2563eb" },
    { label: "Wind Speed", value: `${weather?.wind_speed ?? "--"} km/h`, icon: <MdAir />, color: "#059669" },
    { label: "Precipitation", value: `${weather?.cloud ?? "--"} mm`, icon: <MdCloud />, color: "#7c3aed" },
  ];

  return (
    <>
      <div className="hero-row">
        <div>
          <h1 className="page-title">Live Weather</h1>
          <p className="subtitle">Real-time atmospheric conditions from Open-Meteo.</p>
        </div>

        <select className="select" value={city} onChange={(e) => setCity(e.target.value)}>
          <option value="Kochi">Kochi</option>
          <option value="Kozhikode">Kozhikode</option>
          <option value="Thiruvananthapuram">Thiruvananthapuram</option>
          <option value="Chennai">Chennai</option>
          <option value="Coimbatore">Coimbatore</option>
          <option value="Madurai">Madurai</option>
        </select>
      </div>

      <div className="weather-hero-card">
        <div>
          <p className="label">CURRENT CITY</p>
          <h2>{weather?.city || city}</h2>
          <span>Live sensor stream active</span>
        </div>

        <div className="weather-hero-temp">
          {weather?.temperature ?? "--"}°C
        </div>
      </div>

      <div className="weather-stat-grid">
        {items.map((item) => (
          <div className="weather-stat-card" key={item.label} style={{ borderTopColor: item.color }}>
            <div className="weather-stat-icon" style={{ color: item.color }}>
              {item.icon}
            </div>
            <p>{item.label}</p>
            <h3>{item.value}</h3>
          </div>
        ))}
      </div>

      <Panel title="7 Day Outlook" subtitle="Daily rainfall and temperature forecast">
        <table className="forecast-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Max Temp</th>
              <th>Min Temp</th>
              <th>Rainfall</th>
            </tr>
          </thead>
          <tbody>
            {(weather?.daily?.time || []).map((d, i) => (
              <tr key={d}>
                <td>{d}</td>
                <td>{weather.daily.temperature_2m_max?.[i]}°C</td>
                <td>{weather.daily.temperature_2m_min?.[i]}°C</td>
                <td>{weather.daily.precipitation_sum?.[i]} mm</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}