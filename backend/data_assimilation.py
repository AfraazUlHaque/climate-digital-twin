from risk_engine import (
    flood_score,
    drought_score,
    risk_level,
    flood_advisory,
    drought_advisory,
)


def clamp(value, low=0, high=100):
    return max(low, min(high, float(value)))


class DataAssimilationEngine:
    def __init__(self, model_weight=0.75, obs_weight=0.25):
        self.model_weight = model_weight
        self.obs_weight = obs_weight

    def weather_signal(self, live_weather):
        current = live_weather.get("current", {})

        precipitation = float(current.get("precipitation", 0))
        temperature = float(current.get("temperature", 30))
        humidity = float(current.get("humidity", 0))
        wind_speed = float(current.get("wind_speed", 0))

        # Convert live observation into rainfall signal.
        # This does not replace the model; it corrects it.
        rainfall_signal = (
            precipitation * 6.0
            + max(0, humidity - 70) * 0.08
            + max(0, wind_speed - 20) * 0.03
        )

        return {
            "precipitation": precipitation,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "rainfall_signal": max(0, rainfall_signal),
        }

    def assimilate_forecast(self, model_forecast, live_weather):
        signal = self.weather_signal(live_weather)

        obs_rain = signal["rainfall_signal"]

        model_t1 = float(model_forecast.get("t1", 0))
        model_t3 = float(model_forecast.get("t3", 0))
        model_t7 = float(model_forecast.get("t7", 0))

        assimilated_t1 = self.model_weight * model_t1 + self.obs_weight * obs_rain
        assimilated_t3 = self.model_weight * model_t3 + self.obs_weight * (obs_rain * 0.75)
        assimilated_t7 = self.model_weight * model_t7 + self.obs_weight * (obs_rain * 0.45)

        return {
            "t1": max(0, assimilated_t1),
            "t3": max(0, assimilated_t3),
            "t7": max(0, assimilated_t7),
            "signal": signal,
        }

    def assimilate_summary(self, region, model_summary, live_weather):
        model_forecast = model_summary["forecast"]
        assimilated = self.assimilate_forecast(model_forecast, live_weather)

        flood = flood_score(
            assimilated["t1"],
            assimilated["t3"],
            assimilated["t7"],
            assimilated["signal"]["precipitation"],
        )

        drought = drought_score(
            assimilated["t7"],
            assimilated["signal"]["temperature"],
        )

        return {
            "source": "weighted_gnn_plus_live_weather_assimilation",
            "region": region,
            "date": model_summary.get("date"),
            "weights": {
                "model_weight": self.model_weight,
                "observation_weight": self.obs_weight,
            },
            "model_forecast": model_forecast,
            "assimilated_forecast": {
                "t1": assimilated["t1"],
                "t3": assimilated["t3"],
                "t7": assimilated["t7"],
            },
            "live_observation_signal": assimilated["signal"],
            "risk": {
                "flood": {
                    "score": flood,
                    "level": risk_level(flood),
                    "advisory": flood_advisory(flood),
                },
                "drought": {
                    "score": drought,
                    "level": risk_level(drought),
                    "advisory": drought_advisory(drought),
                },
            },
        }


assimilation_engine = DataAssimilationEngine()