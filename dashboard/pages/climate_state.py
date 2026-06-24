import streamlit as st
import plotly.express as px

from dashboard.utils.data_loader import load_data
from dashboard.components.maps import (
    generate_climate_grid,
    render_climate_map
)
from dashboard.components.charts import (
    observed_rainfall_chart,
    observed_temperature_chart
)


def render():
    rainfall_df, temp_df = load_data()

    st.title("🌍 Current Climate State")

    st.write(
        "This page represents the live virtual state of the climate twin for the selected pilot region."
    )

    col1, col2, col3, col4 = st.columns(4)

    avg_rainfall = rainfall_df["actual"].mean()
    avg_temp = temp_df["actual"].mean()

    col1.metric("Avg Rainfall", f"{avg_rainfall:.2f} mm/day")
    col2.metric("Avg Temperature", f"{avg_temp:.2f} °C")
    col3.metric("Climate Status", "Active")
    col4.metric("Risk Level", "Moderate")

    st.subheader("Observed Climate State Map")

    observed_grid = generate_climate_grid("observed")

    st.plotly_chart(
        render_climate_map(
            observed_grid,
            "Observed Rainfall Distribution",
            "Blues"
        ),
        use_container_width=True
    )

    st.subheader("Climate State Time Series")

    st.plotly_chart(
        observed_rainfall_chart(rainfall_df),
        use_container_width=True
    )

    st.plotly_chart(
        observed_temperature_chart(temp_df),
        use_container_width=True
    )

    st.info(
        "This MVP currently uses generated demo climate fields. Final version will connect this page to IMD/INSAT processed data."
    )