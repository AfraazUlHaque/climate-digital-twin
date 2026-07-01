import { MdAir, MdCloud, MdThermostat, MdWaterDrop } from "react-icons/md";

export default function WeatherCard({ weather }) {
  const w = weather || {};

  return (
    <div className="weather-card clean-weather">
      <div className="weather-main">
        <div>
          <p className="label">CITY</p>
          <h2>{w.city || "Kochi"}</h2>
        </div>

        <div className="weather-temp">{w.temperature ?? "--"}°C</div>
      </div>

      <div className="weather-list">
        <div className="weather-row">
          <MdThermostat />
          <span>Feels like</span>
          <b>{w.feels_like ?? "--"}°C</b>
        </div>

        <div className="weather-row">
          <MdWaterDrop />
          <span>Humidity</span>
          <b>{w.humidity ?? "--"}%</b>
        </div>

        <div className="weather-row">
          <MdAir />
          <span>Wind speed</span>
          <b>{w.wind_speed ?? "--"} km/h</b>
        </div>

        <div className="weather-row">
          <MdCloud />
          <span>Precipitation</span>
          <b>{w.cloud ?? "--"} mm</b>
        </div>
      </div>
    </div>
  );
}