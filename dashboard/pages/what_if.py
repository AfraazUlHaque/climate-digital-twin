import streamlit as st
import numpy as np
import plotly.express as px

from dashboard.utils.data_loader import load_data
from dashboard.utils.helpers import (
    get_risk_level,
    calculate_simulated_temperature,
    calculate_simulated_rainfall
)
from dashboard.components.charts import (
    scenario_temperature_chart,
    rainfall_forecast_chart
)


def generate_climate_grid(mode="observed", temp_increase=0, rainfall_change=0):
    np.random.seed(42)

    base = np.random.normal(loc=65, scale=18, size=(25, 25))
    base = np.clip(base, 0, 140)

    if mode == "scenario":
        grid = base * (1 + rainfall_change / 100) - (temp_increase * 3)
    else:
        grid = base

    return np.clip(grid, -50, 160)


def render_climate_map(grid, title, color_scale="Blues"):
    fig = px.imshow(
        grid,
        color_continuous_scale=color_scale,
        title=title,
        labels=dict(color="Rainfall mm/day")
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig


def render():
    rainfall_df, temp_df = load_data()

    st.title("🧪 What-If Digital Twin Simulator")

    temp_increase = st.slider(
        "Temperature Increase Scenario (°C)",
        0.0,
        7.0,
        2.0,
        0.5
    )

    rainfall_change = st.slider(
        "Rainfall Anomaly (%)",
        -50,
        50,
        10,
        5
    )

    risk = get_risk_level(temp_increase)

    c1, c2, c3 = st.columns(3)
    c1.metric("Temperature Change", f"+{temp_increase}°C")
    c2.metric("Rainfall Anomaly", f"{rainfall_change}%")
    c3.metric("Scenario Risk", risk)

    st.subheader("Twin Response Maps")

    current = generate_climate_grid("observed")
    scenario = generate_climate_grid(
        "scenario",
        temp_increase=temp_increase,
        rainfall_change=rainfall_change
    )
    impact = scenario - current

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(
            render_climate_map(current, "Current Climate State", "Blues"),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            render_climate_map(scenario, "What-If Future State", "OrRd"),
            use_container_width=True
        )

    with col3:
        st.plotly_chart(
            render_climate_map(impact, "Scenario Impact Map", "RdBu"),
            use_container_width=True
        )

    simulated_temp = calculate_simulated_temperature(temp_df, temp_increase)

    st.plotly_chart(
        scenario_temperature_chart(simulated_temp),
        use_container_width=True
    )

    simulated_rainfall = calculate_simulated_rainfall(
        rainfall_df,
        rainfall_change,
        temp_increase
    )

    if "future" in simulated_rainfall.columns:
        simulated_rainfall = simulated_rainfall.rename(
            columns={"future": "predicted"}
        )

    st.plotly_chart(
        rainfall_forecast_chart(simulated_rainfall),
        use_container_width=True
    )