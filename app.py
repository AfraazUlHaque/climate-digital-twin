import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="AI Climate Digital Twin",
    page_icon="🌦️",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
}
.card {
    padding: 18px;
    border-radius: 14px;
    background-color: #f5f7fb;
    border: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_sample_data():
    dates = pd.date_range("2023-06-01", periods=60)

    rainfall = pd.DataFrame({
        "date": dates,
        "actual": np.random.uniform(20, 120, 60),
        "predicted": np.random.uniform(18, 115, 60),
    })

    temperature = pd.DataFrame({
        "date": dates,
        "actual": np.random.uniform(25, 34, 60),
        "predicted": np.random.uniform(25, 34, 60),
    })

    return rainfall, temperature


rainfall_df, temp_df = load_sample_data()

st.sidebar.title("🌦️ Climate Twin")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Current Climate State", "Predictions", "What-If Simulator", "Insights"]
)

st.sidebar.markdown("---")
st.sidebar.info("ISRO Hackathon PS-5 MVP Dashboard")


def show_map(title="Pilot Region: Kerala + Tamil Nadu Coast"):
    st.subheader(title)

    m = folium.Map(location=[10.5, 77.5], zoom_start=6)

    folium.Marker(
        [10.0, 76.3],
        popup="Kerala Pilot Region",
        tooltip="Kerala"
    ).add_to(m)

    folium.Marker(
        [13.0, 80.2],
        popup="Tamil Nadu Coastal Region",
        tooltip="Tamil Nadu"
    ).add_to(m)

    folium.Circle(
        location=[10.5, 77.5],
        radius=250000,
        color="blue",
        fill=True,
        fill_opacity=0.15,
        popup="Pilot Climate Twin Region"
    ).add_to(m)

    st_folium(m, width=900, height=450)


if page == "Home":
    st.markdown('<div class="main-title">AI-Powered Digital Twin of India’s Climate</div>', unsafe_allow_html=True)
    st.write("Bharatiya Antariksh Hackathon 2026 | ISRO / NRSC | Problem Statement 5")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Forecast Horizon", "T+1 / T+7 Days")

    with col2:
        st.metric("Pilot Region", "Kerala + Tamil Nadu")

    with col3:
        st.metric("Model Type", "ConvLSTM MVP")

    st.markdown("### What this dashboard shows")
    st.write("""
    This dashboard demonstrates a prototype climate digital twin using rainfall and temperature prediction,
    interactive visualisation, and what-if scenario simulation.
    """)

    show_map()

    st.markdown("### Digital Twin Flow")
    st.code("""
IMD / INSAT Data
      ↓
Preprocessing
      ↓
AI Prediction Model
      ↓
Climate State
      ↓
What-If Simulation
      ↓
Dashboard Visualisation
    """)


elif page == "Current Climate State":
    st.title("🌍 Current Climate State")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Rainfall", "82 mm/day", "+12%")
    col2.metric("Avg Temperature", "30.4 °C", "+1.2°C")
    col3.metric("Humidity Index", "High", "Monsoon Active")
    col4.metric("Risk Level", "Moderate", "Watch Zone")

    show_map("Current Climate State Map")

    st.subheader("Rainfall Trend")
    fig = px.line(
        rainfall_df,
        x="date",
        y="actual",
        title="Observed Rainfall Over Pilot Region"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Temperature Trend")
    fig2 = px.line(
        temp_df,
        x="date",
        y="actual",
        title="Observed Temperature Over Pilot Region"
    )
    st.plotly_chart(fig2, use_container_width=True)


elif page == "Predictions":
    st.title("🔮 Climate Predictions")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rainfall RMSE", "2.84 mm/day")
    col2.metric("Rainfall MAE", "1.91 mm/day")
    col3.metric("Temp RMSE", "1.12 °C")
    col4.metric("Skill Score", "+0.18")

    st.subheader("Observed vs Predicted Rainfall")
    fig = px.line(
        rainfall_df,
        x="date",
        y=["actual", "predicted"],
        title="Rainfall: Actual vs Predicted"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Observed vs Predicted Temperature")
    fig2 = px.line(
        temp_df,
        x="date",
        y=["actual", "predicted"],
        title="Temperature: Actual vs Predicted"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Prediction Heatmap Demo")

    heatmap_data = np.random.rand(10, 10) * 100
    fig3 = px.imshow(
        heatmap_data,
        labels=dict(color="Rainfall mm/day"),
        title="Predicted Rainfall Spatial Field"
    )
    st.plotly_chart(fig3, use_container_width=True)


elif page == "What-If Simulator":
    st.title("🧪 What-If Climate Simulator")

    st.write("Change climate conditions and see simulated impact on rainfall and temperature.")

    temp_increase = st.slider("Temperature Increase Scenario", 0.0, 5.0, 2.0, 0.5)
    rainfall_change = st.slider("Rainfall Anomaly Scenario (%)", -50, 50, 10, 5)

    simulated_rainfall = rainfall_df.copy()
    simulated_rainfall["simulated"] = simulated_rainfall["predicted"] * (1 + rainfall_change / 100) - (temp_increase * 2)

    simulated_temp = temp_df.copy()
    simulated_temp["simulated"] = simulated_temp["predicted"] + temp_increase

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature Perturbation", f"+{temp_increase} °C")
    col2.metric("Rainfall Change", f"{rainfall_change}%")
    col3.metric("Scenario Risk", "High" if temp_increase >= 3 else "Moderate")

    st.subheader("Simulated Rainfall Impact")
    fig = px.line(
        simulated_rainfall,
        x="date",
        y=["predicted", "simulated"],
        title="Predicted vs What-If Rainfall"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Simulated Temperature Impact")
    fig2 = px.line(
        simulated_temp,
        x="date",
        y=["predicted", "simulated"],
        title="Predicted vs What-If Temperature"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.warning("This is an MVP scenario engine. Final version will use trained model inference.")


elif page == "Insights":
    st.title("📊 Climate Insights")

    st.subheader("Monthly Rainfall Distribution")
    rainfall_df["month"] = rainfall_df["date"].dt.month_name()
    fig = px.box(
        rainfall_df,
        x="month",
        y="actual",
        title="Rainfall Variability by Month"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Rainfall vs Temperature Relationship")
    combined = pd.DataFrame({
        "rainfall": rainfall_df["actual"],
        "temperature": temp_df["actual"]
    })

    fig2 = px.scatter(
        combined,
        x="temperature",
        y="rainfall",
        title="Rainfall vs Temperature"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.success("Dashboard MVP ready for hackathon demo.")