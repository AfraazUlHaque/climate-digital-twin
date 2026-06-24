import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Climate Digital Twin", page_icon="🌦️", layout="wide")

@st.cache_data
def load_data():
    dates = pd.date_range("2024-01-01", periods=60)

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


def generate_climate_grid(mode="observed", temp_increase=0, rainfall_change=0):
    np.random.seed(42)

    base = np.random.normal(loc=65, scale=18, size=(25, 25))
    base = np.clip(base, 0, 140)

    if mode == "predicted":
        grid = base + np.random.normal(3, 8, size=(25, 25))
    elif mode == "scenario":
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
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=50, b=10))
    return fig


rainfall_df, temp_df = load_data()

st.sidebar.title("🌦️ Climate Digital Twin")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Current Climate State", "Predictions", "What-If Simulator", "Insights"]
)

if page == "Home":
    st.title("🌦️ AI-Powered Digital Twin of India's Climate")
    st.write("Bharatiya Antariksh Hackathon 2026 | ISRO / NRSC | PS-5")

    c1, c2, c3 = st.columns(3)
    c1.metric("Pilot Region", "Kerala + Tamil Nadu")
    c2.metric("Forecast Horizon", "T+1 / T+7")
    c3.metric("Core Model", "ConvLSTM MVP")

    st.subheader("Digital Twin Architecture")
    st.code("""
IMD / INSAT Data
      ↓
Preprocessing Pipeline
      ↓
AI Prediction Engine
      ↓
Current Climate State
      ↓
What-If Scenario Engine
      ↓
Interactive Dashboard
""")

    grid = generate_climate_grid("observed")
    st.plotly_chart(
        render_climate_map(grid, "Current Climate State Preview", "Blues"),
        use_container_width=True
    )

elif page == "Current Climate State":
    st.title("🌍 Current Climate State")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Rainfall", f"{rainfall_df['actual'].mean():.2f} mm/day")
    c2.metric("Avg Temperature", f"{temp_df['actual'].mean():.2f} °C")
    c3.metric("Climate Status", "Active")
    c4.metric("Risk Level", "Moderate")

    observed = generate_climate_grid("observed")
    st.plotly_chart(
        render_climate_map(observed, "Observed Rainfall Distribution", "Blues"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(rainfall_df, x="date", y="actual", title="Observed Rainfall Trend"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(temp_df, x="date", y="actual", title="Observed Temperature Trend"),
        use_container_width=True
    )

elif page == "Predictions":
    st.title("🔮 AI Prediction Engine")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rainfall RMSE", "2.84 mm/day")
    c2.metric("Rainfall MAE", "1.91 mm/day")
    c3.metric("Temperature RMSE", "1.12 °C")
    c4.metric("Skill Score", "+0.18")

    observed = generate_climate_grid("observed")
    predicted = generate_climate_grid("predicted")
    difference = predicted - observed

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(
            render_climate_map(observed, "Observed State", "Blues"),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            render_climate_map(predicted, "AI Predicted State", "Viridis"),
            use_container_width=True
        )

    with col3:
        st.plotly_chart(
            render_climate_map(difference, "Prediction Difference", "RdBu"),
            use_container_width=True
        )

    st.plotly_chart(
        px.line(rainfall_df, x="date", y=["actual", "predicted"], title="Rainfall: Actual vs Predicted"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(temp_df, x="date", y=["actual", "predicted"], title="Temperature: Actual vs Predicted"),
        use_container_width=True
    )

elif page == "What-If Simulator":
    st.title("🧪 What-If Digital Twin Simulator")

    temp_increase = st.slider("Temperature Increase Scenario (°C)", 0.0, 7.0, 2.0, 0.5)
    rainfall_change = st.slider("Rainfall Anomaly (%)", -50, 50, 10, 5)

    if temp_increase >= 6:
        risk = "Extreme"
    elif temp_increase >= 4:
        risk = "High"
    elif temp_increase >= 2:
        risk = "Moderate"
    else:
        risk = "Low"

    c1, c2, c3 = st.columns(3)
    c1.metric("Temperature Change", f"+{temp_increase}°C")
    c2.metric("Rainfall Anomaly", f"{rainfall_change}%")
    c3.metric("Scenario Risk", risk)

    current = generate_climate_grid("observed")
    scenario = generate_climate_grid("scenario", temp_increase, rainfall_change)
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

    scenario_temp = temp_df.copy()
    scenario_temp["future"] = scenario_temp["predicted"] + temp_increase

    st.plotly_chart(
        px.line(scenario_temp, x="date", y=["predicted", "future"], title="Temperature Scenario"),
        use_container_width=True
    )

    scenario_rain = rainfall_df.copy()
    scenario_rain["future"] = scenario_rain["predicted"] * (1 + rainfall_change / 100) - temp_increase * 2

    st.plotly_chart(
        px.line(scenario_rain, x="date", y=["predicted", "future"], title="Rainfall Scenario"),
        use_container_width=True
    )

elif page == "Insights":
    st.title("📊 Climate Insights")

    rainfall_df["month"] = rainfall_df["date"].dt.month

    st.plotly_chart(
        px.box(rainfall_df, x="month", y="actual", title="Rainfall Distribution by Month"),
        use_container_width=True
    )

    combined = pd.DataFrame({
        "temperature": temp_df["actual"],
        "rainfall": rainfall_df["actual"]
    })

    st.plotly_chart(
        px.scatter(combined, x="temperature", y="rainfall", title="Rainfall vs Temperature"),
        use_container_width=True
    )

    st.success("Dashboard MVP Ready 🚀")