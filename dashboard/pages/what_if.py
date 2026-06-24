import streamlit as st

st.title("🧪 What-If Simulator")

temp = st.slider(
    "Increase Temperature",
    0,
    7,
    2
)

rain = st.slider(
    "Rainfall Change %",
    -50,
    50,
    10
)

st.write(
    f"Scenario: +{temp}°C and {rain}% rainfall anomaly"
)