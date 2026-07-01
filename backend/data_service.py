import pandas as pd
from fastapi import HTTPException

from config import PREDICTION_CSV_PATHS
from risk_engine import flood_score, drought_score


def first_existing(paths, name):
    for path in paths:
        if path.exists():
            return path

    raise FileNotFoundError(
        f"{name} not found. Checked:\n" + "\n".join(str(p) for p in paths)
    )


class DataService:
    def __init__(self):
        self.df = None
        self.csv_path = None
        self.feature_cols = None

    def load(self):
        if self.df is not None:
            return self.df

        self.csv_path = first_existing(
            PREDICTION_CSV_PATHS,
            "weighted_gnn_predictions.csv",
        )

        df = pd.read_csv(self.csv_path)

        rename_map = {
            "pred_t1": "predicted_t1",
            "pred_t3": "predicted_t3",
            "pred_t7": "predicted_t7",
            "target_t1": "actual_t1",
            "target_t3": "actual_t3",
            "target_t7": "actual_t7",
        }

        df = df.rename(columns=rename_map)

        required = ["date", "region", "lat", "lon"]

        for col in required:
            if col not in df.columns:
                raise RuntimeError(f"Missing CSV column: {col}")

        for col in ["predicted_t1", "predicted_t3", "predicted_t7"]:
            if col not in df.columns:
                raise RuntimeError(f"Missing prediction column: {col}")

        df["date"] = pd.to_datetime(df["date"])

        if "actual_t1" not in df.columns:
            df["actual_t1"] = 0
        if "actual_t3" not in df.columns:
            df["actual_t3"] = 0
        if "actual_t7" not in df.columns:
            df["actual_t7"] = 0

        if "flood_risk_index" not in df.columns:
            df["flood_risk_index"] = df.apply(
                lambda r: flood_score(
                    r["predicted_t1"],
                    r["predicted_t3"],
                    r["predicted_t7"],
                ),
                axis=1,
            )

        if "drought_risk_index" not in df.columns:
            df["drought_risk_index"] = df.apply(
                lambda r: drought_score(r["predicted_t7"]),
                axis=1,
            )

        self.df = df

        # Features for model inference:
        # remove metadata + targets/preds/risk columns
        ignore_cols = {
            "date",
            "region",
            "lat",
            "lon",
            "actual_t1",
            "actual_t3",
            "actual_t7",
            "predicted_t1",
            "predicted_t3",
            "predicted_t7",
            "flood_risk_index",
            "drought_risk_index",
        }

        numeric_cols = [
            c for c in df.columns
            if c not in ignore_cols and pd.api.types.is_numeric_dtype(df[c])
        ]

        self.feature_cols = numeric_cols

        print("✅ Data loaded:", self.csv_path)
        print("Rows:", len(df))
        print("Feature cols:", self.feature_cols)

        return self.df

    def get_regions(self):
        df = self.load()
        return sorted(df["region"].dropna().unique().tolist())

    def get_dates(self, region=None):
        df = self.load()

        if region:
            df = df[df["region"] == region]

        return sorted(df["date"].dt.strftime("%Y-%m-%d").unique().tolist())

    def latest_date(self, region):
        df = self.load()
        data = df[df["region"] == region]

        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data for region {region}")

        return data["date"].max()

    def get_filtered(self, region, date=None):
        df = self.load()

        data = df[df["region"] == region].copy()

        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data for region {region}")

        if date is None:
            selected_date = data["date"].max()
        else:
            selected_date = pd.to_datetime(date)

        data = data[data["date"] == selected_date]

        if data.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data for {region} on {selected_date.date()}",
            )

        return data

    def history_source(self, region, limit=180):
        df = self.load()
        data = df[df["region"] == region].copy()

        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data for region {region}")

        daily = (
            data.groupby("date", as_index=False)
            .agg({
                "actual_t1": "mean",
                "predicted_t1": "mean",
                "actual_t3": "mean",
                "predicted_t3": "mean",
                "actual_t7": "mean",
                "predicted_t7": "mean",
                "flood_risk_index": "mean",
                "drought_risk_index": "mean",
            })
            .tail(limit)
        )

        daily["date"] = daily["date"].dt.strftime("%Y-%m-%d")

        return daily.to_dict(orient="records")


data_service = DataService()