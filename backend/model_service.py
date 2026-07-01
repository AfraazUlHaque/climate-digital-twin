import joblib
import torch

from config import (
    DEVICE,
    MODEL_PATHS,
    X_SCALER_PATHS,
    Y_SCALER_PATHS,
    GRAPH_PATHS,
)
from model_def import ClimateWeightedGNN


def first_existing(paths, name):
    for path in paths:
        if path.exists():
            return path

    raise FileNotFoundError(
        f"{name} not found. Checked:\n" + "\n".join(str(p) for p in paths)
    )


class ModelService:
    def __init__(self):
        self.loaded = False

        self.model = None
        self.x_scaler = None
        self.y_scaler = None

        self.graph_bundle = None
        self.graphs = None
        self.feature_cols = None
        self.target_cols = None

        self.model_path = None
        self.x_scaler_path = None
        self.y_scaler_path = None
        self.graph_path = None

        self.input_dim = None
        self.output_dim = None

    def load(self):
        if self.loaded:
            return self

        self.model_path = first_existing(MODEL_PATHS, "weighted_gnn_best.pt")
        self.x_scaler_path = first_existing(X_SCALER_PATHS, "weighted_gnn_x_scaler.pkl")
        self.y_scaler_path = first_existing(Y_SCALER_PATHS, "weighted_gnn_y_scaler.pkl")
        self.graph_path = first_existing(GRAPH_PATHS, "climate_graphs_weighted.pt")

        self.graph_bundle = torch.load(self.graph_path, map_location=DEVICE)

        if not isinstance(self.graph_bundle, dict):
            raise RuntimeError("Graph file must be a dictionary.")

        if "graphs" not in self.graph_bundle:
            raise RuntimeError("Graph file missing key: graphs")

        self.graphs = self.graph_bundle["graphs"]
        self.feature_cols = self.graph_bundle.get("feature_cols", None)
        self.target_cols = self.graph_bundle.get(
            "target_cols",
            ["target_rainfall_t1", "target_rainfall_t3", "target_rainfall_t7"],
        )

        if not self.graphs:
            raise RuntimeError("No graphs found inside climate_graphs_weighted.pt")

        first_graph = self.graphs[0]

        if self.feature_cols is None:
            self.input_dim = int(first_graph["x"].shape[1])
            self.feature_cols = [f"feature_{i}" for i in range(self.input_dim)]
        else:
            self.input_dim = len(self.feature_cols)

        self.output_dim = len(self.target_cols)

        self.model = ClimateWeightedGNN(
            in_dim=self.input_dim,
            hidden_dim=64,
            out_dim=self.output_dim,
        ).to(DEVICE)

        state = torch.load(self.model_path, map_location=DEVICE)

        if isinstance(state, dict) and "state_dict" in state:
            state = state["state_dict"]

        self.model.load_state_dict(state)
        self.model.eval()

        self.x_scaler = joblib.load(self.x_scaler_path)
        self.y_scaler = joblib.load(self.y_scaler_path)

        self.loaded = True

        print("✅ Weighted GNN loaded with trained graph")
        print("Model:", self.model_path)
        print("Graph:", self.graph_path)
        print("X scaler:", self.x_scaler_path)
        print("Y scaler:", self.y_scaler_path)
        print("Graphs:", len(self.graphs))
        print("Input dim:", self.input_dim)
        print("Output dim:", self.output_dim)
        print("Features:", self.feature_cols)
        print("Targets:", self.target_cols)

        return self

    def get_graph_by_date(self, date=None):
        self.load()

        if date is None:
            return self.graphs[-1]

        date = str(date)

        for graph in self.graphs:
            meta = graph.get("meta", {})
            graph_date = str(meta.get("date", ""))

            if graph_date == date:
                return graph

        return self.graphs[-1]


model_service = ModelService()