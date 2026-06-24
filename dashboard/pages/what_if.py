import streamlit as st
import plotly.express as px

from dashboard.utils.data_loader import load_data

def render():

    _, temp_df = load_data()

    st.title("🧪 What-If Simulator")

    temp_increase = st.slider(
        "Temperature Increase",
        0.0,
        7.0,
        2.0,
        0.5
    )

    scenario = temp_df.copy()

    scenario["future"] = (
        scenario["predicted"]
        + temp_increase
    )

    fig = px.line(
        scenario,
        x="date",
        y=["predicted", "future"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )