import pandas as pd
import numpy as np

def load_data():

    dates = pd.date_range(
        "2024-01-01",
        periods=60
    )

    rainfall = pd.DataFrame({
        "date": dates,
        "actual": np.random.uniform(20, 100, 60),
        "predicted": np.random.uniform(20, 100, 60)
    })

    temperature = pd.DataFrame({
        "date": dates,
        "actual": np.random.uniform(24, 35, 60),
        "predicted": np.random.uniform(24, 35, 60)
    })

    return rainfall, temperature