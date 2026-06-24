import streamlit as st
import plotly.express as px

from dashboard.components.maps import generate_climate_grid, render_climate_map
from dashboard.utils.data_loader import load_data
from dashboard.components.charts import rainfall_forecast_chart, temperature_forecast_chart


def render():
    rainfall_df, temp_df = load_data()

    st.title("🔮 AI Prediction Engine")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rainfall RMSE", "2.84 mm/day")
    c2.metric("Rainfall MAE", "1.91 mm/day")
    c3.metric("Temp RMSE", "1.12 °C")
    c4.metric("Skill Score", "+0.18")

    st.subheader("Digital Twin Forecast Maps")

    observed = generate_climate_grid("observed")
    predicted = generate_climate_grid("predicted")
    difference = predicted - observed

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(
            render_climate_map(observed, "Observed Climate State", "Blues"),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            render_climate_map(predicted, "AI Predicted State", "Viridis"),
            use_container_width=True
        )

    with col3:
        st.plotly_chart(
            render_climate_map(difference, "Prediction Difference Map", "RdBu"),
            use_container_width=True
        )

    st.subheader("Forecast Time Series")

    st.plotly_chart(
        rainfall_forecast_chart(rainfall_df),
        use_container_width=True
    )

    st.plotly_chart(
        temperature_forecast_chart(temp_df),
        use_container_width=True
    )