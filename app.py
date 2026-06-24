import streamlit as st

from dashboard.pages import (
    home,
    climate_state,
    predictions,
    what_if,
    insights
)

st.set_page_config(
    page_title="Climate Digital Twin",
    page_icon="🌦️",
    layout="wide"
)

st.sidebar.title("🌦️ Climate Digital Twin")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Current Climate State",
        "Predictions",
        "What-If Simulator",
        "Insights"
    ]
)

if page == "Home":
    home.render()

elif page == "Current Climate State":
    climate_state.render()

elif page == "Predictions":
    predictions.render()

elif page == "What-If Simulator":
    what_if.render()

elif page == "Insights":
    insights.render()