import numpy as np
import torch
from fastapi import HTTPException

from config import DEVICE
from model_service import model_service
from risk_engine import (
    flood_score,
    drought_score,
    risk_level,
    flood_advisory,
    drought_advisory,
)


class PredictionService:
    def __init__(self):
        model_service.load()

    def _get_meta_value(self, meta, key, index, default=None):
        value = meta.get(key, default)

        if isinstance(value, (list, tuple)):
            return value[index]

        try:
            if hasattr(value, "__len__") and not isinstance(value, str):
                return value[index]
        except Exception:
            pass

        return value

    def _mutate_features(self, x_raw, rainfall_change=0, temp_change=0):
        x_mut = x_raw.copy()
        feature_cols = model_service.feature_cols

        for idx, col in enumerate(feature_cols):
            name = str(col).lower()

            if "rain" in name or "precip" in name:
                x_mut[:, idx] = np.clip(
                    x_mut[:, idx] * (1 + float(rainfall_change) / 100),
                    0,
                    None,
                )

            if any(k in name for k in ["temp", "tmax", "tmin"]):
                x_mut[:, idx] = x_mut[:, idx] + float(temp_change)

        return x_mut

    def _run_model_on_graph(self, graph, rainfall_change=0, temp_change=0):
        model_service.load()

        x_raw = graph["x"].detach().cpu().numpy().astype(float)
        x_raw = self._mutate_features(x_raw, rainfall_change, temp_change)

        x_scaled = model_service.x_scaler.transform(x_raw)
        x = torch.tensor(x_scaled, dtype=torch.float32).to(DEVICE)

        edge_index = graph["edge_index"].long().to(DEVICE)

        if "edge_weight" in graph:
            edge_weight = graph["edge_weight"].float().to(DEVICE)
        else:
            edge_weight = torch.ones(edge_index.shape[1], dtype=torch.float32).to(DEVICE)

        with torch.no_grad():
            pred_scaled = model_service.model(x, edge_index, edge_weight).cpu().numpy()

        pred = model_service.y_scaler.inverse_transform(pred_scaled)
        pred = np.clip(pred, 0, None)

        return pred

    def regions(self):
        model_service.load()
        graph = model_service.graphs[-1]
        meta = graph.get("meta", {})

        regions = meta.get("regions") or meta.get("region")

        if regions is None:
            return ["Kerala", "Tamil Nadu"]

        return sorted(list(set(list(regions))))

    def dates(self):
        model_service.load()

        dates = []

        for graph in model_service.graphs:
            meta = graph.get("meta", {})
            if "date" in meta:
                dates.append(str(meta["date"]))

        return dates

    def predict_rows(
        self,
        region="Kerala",
        date=None,
        rainfall_change=0,
        temp_change=0,
        apply_scenario_to_risk=False,
    ):
        graph = model_service.get_graph_by_date(date)

        pred = self._run_model_on_graph(
            graph,
            rainfall_change=rainfall_change,
            temp_change=temp_change,
        )

        meta = graph.get("meta", {})
        rows = []

        rain_factor = 1 + float(rainfall_change) / 100

        for i in range(pred.shape[0]):
            row_region = self._get_meta_value(meta, "regions", i, None)

            if row_region is None:
                row_region = self._get_meta_value(meta, "region", i, region)

            if str(row_region) != str(region):
                continue

            lat = self._get_meta_value(meta, "lat", i, 0)
            lon = self._get_meta_value(meta, "lon", i, 0)

            t1 = float(pred[i, 0])
            t3 = float(pred[i, 1]) if pred.shape[1] > 1 else t1
            t7 = float(pred[i, 2]) if pred.shape[1] > 2 else t3

            if apply_scenario_to_risk:
                scenario_t1 = max(0, t1 * rain_factor)
                scenario_t3 = max(0, t3 * rain_factor)
                scenario_t7 = max(0, t7 * rain_factor)
            else:
                scenario_t1 = t1
                scenario_t3 = t3
                scenario_t7 = t7

            flood = flood_score(scenario_t1, scenario_t3, scenario_t7)
            drought = drought_score(scenario_t7, 30 + float(temp_change))

            rows.append({
                "date": str(meta.get("date", "")),
                "region": str(row_region),
                "lat": float(lat),
                "lon": float(lon),
                "predicted_t1": scenario_t1,
                "predicted_t3": scenario_t3,
                "predicted_t7": scenario_t7,
                "raw_model_t1": t1,
                "raw_model_t3": t3,
                "raw_model_t7": t7,
                "flood_risk_index": flood,
                "drought_risk_index": drought,
            })

        if not rows:
            raise HTTPException(status_code=404, detail=f"No rows found for region: {region}")

        return rows

    def summary(self, region="Kerala", date=None):
        rows = self.predict_rows(region, date)

        t1 = float(np.mean([r["predicted_t1"] for r in rows]))
        t3 = float(np.mean([r["predicted_t3"] for r in rows]))
        t7 = float(np.mean([r["predicted_t7"] for r in rows]))

        flood = float(np.mean([r["flood_risk_index"] for r in rows]))
        drought = float(np.mean([r["drought_risk_index"] for r in rows]))

        return {
            "source": "weighted_gnn_model_with_trained_graph",
            "region": region,
            "date": rows[0]["date"],
            "grid_cells": len(rows),
            "forecast": {
                "t1": t1,
                "t3": t3,
                "t7": t7,
            },
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

    def history(self, region="Kerala", limit=120):
        model_service.load()

        out = []
        graphs = model_service.graphs[-limit:]

        for graph in graphs:
            try:
                date = graph.get("meta", {}).get("date")
                summary = self.summary(region, date)

                out.append({
                    "date": summary["date"],
                    "actual_t1": 0,
                    "predicted_t1": summary["forecast"]["t1"],
                    "actual_t3": 0,
                    "predicted_t3": summary["forecast"]["t3"],
                    "actual_t7": 0,
                    "predicted_t7": summary["forecast"]["t7"],
                    "flood_risk_index": summary["risk"]["flood"]["score"],
                    "drought_risk_index": summary["risk"]["drought"]["score"],
                })

            except Exception:
                continue

        return out

    def map_data(self, region="Kerala", date=None):
        return self.predict_rows(region, date)

    def what_if(self, payload):
        region = payload.get("region", "Kerala")
        date = payload.get("date", None)

        rainfall_change = float(payload.get("rainfall_change", 0))
        temp_change = float(payload.get("temperature_change", payload.get("temp_change", 0)))

        rows = self.predict_rows(
            region=region,
            date=date,
            rainfall_change=rainfall_change,
            temp_change=temp_change,
            apply_scenario_to_risk=True,
        )

        t1 = float(np.mean([r["predicted_t1"] for r in rows]))
        t3 = float(np.mean([r["predicted_t3"] for r in rows]))
        t7 = float(np.mean([r["predicted_t7"] for r in rows]))

        flood = float(np.mean([r["flood_risk_index"] for r in rows]))
        drought = float(np.mean([r["drought_risk_index"] for r in rows]))

        return {
            "source": "weighted_gnn_model_what_if_with_trained_graph",
            "region": region,
            "date": rows[0]["date"],
            "grid_cells": len(rows),
            "scenario": {
                "rainfall_change": rainfall_change,
                "temperature_change": temp_change,
            },
            "scenario_forecast": {
                "t1": t1,
                "t3": t3,
                "t7": t7,
            },
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
        }

    def what_if_map(self, payload):
        region = payload.get("region", "Kerala")
        date = payload.get("date", None)

        rainfall_change = float(payload.get("rainfall_change", 0))
        temp_change = float(payload.get("temperature_change", payload.get("temp_change", 0)))

        rows = self.predict_rows(
            region=region,
            date=date,
            rainfall_change=rainfall_change,
            temp_change=temp_change,
            apply_scenario_to_risk=True,
        )

        if len(rows) > 300:
            step = max(1, len(rows) // 300)
            rows = rows[::step]

        return {
            "source": "weighted_gnn_model_heatmap",
            "region": region,
            "date": rows[0]["date"],
            "scenario": {
                "rainfall_change": rainfall_change,
                "temperature_change": temp_change,
            },
            "points": rows,
        }

    def what_if_grid(self, payload):
        region = payload.get("region", "Kerala")
        date = payload.get("date", None)

        rainfall_change = float(payload.get("rainfall_change", 0))
        temp_change = float(payload.get("temperature_change", payload.get("temp_change", 0)))

        baseline = self.predict_rows(
            region=region,
            date=date,
            rainfall_change=0,
            temp_change=0,
            apply_scenario_to_risk=False,
        )

        scenario = self.predict_rows(
            region=region,
            date=date,
            rainfall_change=rainfall_change,
            temp_change=temp_change,
            apply_scenario_to_risk=True,
        )

        points = []

        for b, s in zip(baseline, scenario):
            points.append({
                "region": region,
                "date": s["date"],
                "lat": s["lat"],
                "lon": s["lon"],

                "baseline_t1": b["predicted_t1"],
                "baseline_t3": b["predicted_t3"],
                "baseline_t7": b["predicted_t7"],

                "scenario_t1": s["predicted_t1"],
                "scenario_t3": s["predicted_t3"],
                "scenario_t7": s["predicted_t7"],

                "baseline_flood": b["flood_risk_index"],
                "scenario_flood": s["flood_risk_index"],

                "baseline_drought": b["drought_risk_index"],
                "scenario_drought": s["drought_risk_index"],

                "delta_rainfall": s["predicted_t7"] - b["predicted_t7"],
                "delta_flood": s["flood_risk_index"] - b["flood_risk_index"],
                "delta_drought": s["drought_risk_index"] - b["drought_risk_index"],
            })

        if len(points) > 400:
            step = max(1, len(points) // 400)
            points = points[::step]

        def avg(key):
            return sum(float(p[key]) for p in points) / max(len(points), 1)

        return {
            "source": "trained_weighted_gnn_counterfactual",
            "region": region,
            "date": points[0]["date"] if points else date,
            "scenario": {
                "rainfall_change": rainfall_change,
                "temperature_change": temp_change,
            },
            "summary": {
                "baseline_t1": avg("baseline_t1"),
                "baseline_t3": avg("baseline_t3"),
                "baseline_t7": avg("baseline_t7"),

                "scenario_t1": avg("scenario_t1"),
                "scenario_t3": avg("scenario_t3"),
                "scenario_t7": avg("scenario_t7"),

                "baseline_flood": avg("baseline_flood"),
                "scenario_flood": avg("scenario_flood"),

                "baseline_drought": avg("baseline_drought"),
                "scenario_drought": avg("scenario_drought"),

                "delta_rainfall": avg("delta_rainfall"),
                "delta_flood": avg("delta_flood"),
                "delta_drought": avg("delta_drought"),
            },
            "points": points,
        }


prediction_service = PredictionService()