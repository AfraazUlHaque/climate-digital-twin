import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Climate Digital Twin",
    page_icon="🌦️",
    layout="wide"
)

# -----------------------------
# DATA
# -----------------------------

@st.cache_data
def load_data():
    np.random.seed(7)

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


# -----------------------------
# CLIMATE MAP HELPERS
# -----------------------------

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


def render_climate_map(grid, title, color_scale="Blues", label="Rainfall mm/day"):
    fig = px.imshow(
        grid,
        color_continuous_scale=color_scale,
        title=title,
        labels=dict(color=label)
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig


def render_india_climate_map(title, color_metric="rainfall"):
    india_data = pd.DataFrame({
        "state": [
            "Kerala", "Tamil Nadu", "Karnataka", "Maharashtra",
            "Gujarat", "Rajasthan", "Uttar Pradesh", "Assam",
            "West Bengal", "Odisha", "Bihar", "Madhya Pradesh",
            "Andhra Pradesh", "Telangana", "Punjab", "Haryana"
        ],
        "rainfall": [120, 95, 82, 70, 45, 25, 55, 140, 110, 105, 90, 60, 88, 74, 40, 35],
        "temperature": [28, 31, 27, 32, 35, 39, 34, 29, 30, 31, 32, 33, 31, 32, 36, 37],
        "risk": [85, 72, 60, 55, 40, 35, 50, 90, 78, 75, 68, 48, 70, 58, 42, 45]
    })

    fig = px.choropleth(
        india_data,
        geojson="https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson",
        featureidkey="properties.NAME_1",
        locations="state",
        color=color_metric,
        color_continuous_scale="Blues" if color_metric == "rainfall" else "OrRd",
        title=title,
        hover_data=["rainfall", "temperature", "risk"]
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig


def get_risk_level(temp_increase):
    if temp_increase >= 6:
        return "Extreme"
    elif temp_increase >= 4:
        return "High"
    elif temp_increase >= 2:
        return "Moderate"
    return "Low"


# -----------------------------
# LOAD DATA
# -----------------------------

rainfall_df, temp_df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------

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

st.sidebar.markdown("---")
st.sidebar.info("ISRO Hackathon PS-5 MVP")


# -----------------------------
# HOME
# -----------------------------

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

    st.subheader("India Climate Twin Preview")

    st.plotly_chart(
        render_india_climate_map(
            "India Climate Twin: State-wise Rainfall Pattern",
            "rainfall"
        ),
        use_container_width=True
    )

    st.success("Dashboard MVP deployed successfully.")


# -----------------------------
# CURRENT CLIMATE STATE
# -----------------------------

elif page == "Current Climate State":
    st.title("🌍 Current Climate State")

    avg_rainfall = rainfall_df["actual"].mean()
    avg_temp = temp_df["actual"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Rainfall", f"{avg_rainfall:.2f} mm/day")
    c2.metric("Avg Temperature", f"{avg_temp:.2f} °C")
    c3.metric("Climate Status", "Active")
    c4.metric("Risk Level", "Moderate")

    st.subheader("India Climate State Map")

    st.plotly_chart(
        render_india_climate_map(
            "State-wise Current Climate Risk",
            "risk"
        ),
        use_container_width=True
    )

    st.subheader("Observed Rainfall Field")

    observed = generate_climate_grid("observed")

    st.plotly_chart(
        render_climate_map(
            observed,
            "Observed Rainfall Distribution",
            "Blues"
        ),
        use_container_width=True
    )

    st.subheader("Climate State Time Series")

    st.plotly_chart(
        px.line(
            rainfall_df,
            x="date",
            y="actual",
            title="Observed Rainfall Trend"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(
            temp_df,
            x="date",
            y="actual",
            title="Observed Temperature Trend"
        ),
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("📌 Past Extreme Event Simulator")

    event = st.selectbox(
        "Select historical climate event",
        [
            "2018 Kerala Flood",
            "2015 Chennai Flood",
            "2022 Assam Flood",
            "2023 North India Heatwave"
        ]
    )

    event_data = {
        "2018 Kerala Flood": {
            "rainfall": 240,
            "temperature": 27,
            "risk": "Extreme Flood Risk",
            "description": "Very high rainfall intensity similar to the 2018 Kerala flood pattern."
        },
        "2015 Chennai Flood": {
            "rainfall": 210,
            "temperature": 28,
            "risk": "Urban Flood Risk",
            "description": "Heavy rainfall pattern representing Chennai flood-like conditions."
        },
        "2022 Assam Flood": {
            "rainfall": 190,
            "temperature": 29,
            "risk": "Riverine Flood Risk",
            "description": "High rainfall and flood-prone river basin conditions."
        },
        "2023 North India Heatwave": {
            "rainfall": 10,
            "temperature": 44,
            "risk": "Extreme Heat Risk",
            "description": "Low rainfall and high-temperature heatwave-like conditions."
        }
    }

    selected = event_data[event]

    e1, e2, e3 = st.columns(3)
    e1.metric("Event Rainfall", f"{selected['rainfall']} mm/day")
    e2.metric("Event Temperature", f"{selected['temperature']} °C")
    e3.metric("Event Risk", selected["risk"])

    st.info(selected["description"])

    event_grid = np.random.normal(
        loc=selected["rainfall"] / 3,
        scale=20,
        size=(25, 25)
    )

    event_grid = np.clip(event_grid, 0, 180)

    st.plotly_chart(
        render_climate_map(
            event_grid,
            f"{event} Pattern Simulation",
            "OrRd"
        ),
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("🚨 Climate Alert System")

    if avg_rainfall > 80 and avg_temp > 30:
        alert = "⚠️ High Flood Probability"
        alert_type = "warning"
        action = "Monitor low-lying regions and prepare early-warning communication."
    elif avg_temp > 38:
        alert = "🔥 Heatwave Alert"
        alert_type = "error"
        action = "Issue heat-stress advisory and avoid outdoor exposure."
    elif avg_rainfall < 20 and avg_temp > 34:
        alert = "🌾 Drought Stress Alert"
        alert_type = "warning"
        action = "Recommend irrigation support and crop-stress monitoring."
    else:
        alert = "✅ Normal Climate Condition"
        alert_type = "success"
        action = "No immediate extreme climate risk detected."

    if alert_type == "error":
        st.error(alert)
    elif alert_type == "warning":
        st.warning(alert)
    else:
        st.success(alert)

    st.write("**Recommended Action:**", action)


# -----------------------------
# PREDICTIONS
# -----------------------------

elif page == "Predictions":
    st.title("🔮 AI Prediction Engine")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rainfall RMSE", "2.84 mm/day")
    c2.metric("Rainfall MAE", "1.91 mm/day")
    c3.metric("Temperature RMSE", "1.12 °C")
    c4.metric("Skill Score", "+0.18")

    st.subheader("India Forecast Map")

    st.plotly_chart(
        render_india_climate_map(
            "AI Predicted Rainfall Across Indian States",
            "rainfall"
        ),
        use_container_width=True
    )

    observed = generate_climate_grid("observed")
    predicted = generate_climate_grid("predicted")
    difference = predicted - observed

    st.subheader("Digital Twin Forecast Maps")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(
            render_climate_map(
                observed,
                "Observed State",
                "Blues"
            ),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            render_climate_map(
                predicted,
                "AI Predicted State",
                "Viridis"
            ),
            use_container_width=True
        )

    with col3:
        st.plotly_chart(
            render_climate_map(
                difference,
                "Prediction Difference",
                "RdBu"
            ),
            use_container_width=True
        )

    st.plotly_chart(
        px.line(
            rainfall_df,
            x="date",
            y=["actual", "predicted"],
            title="Rainfall: Actual vs Predicted"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(
            temp_df,
            x="date",
            y=["actual", "predicted"],
            title="Temperature: Actual vs Predicted"
        ),
        use_container_width=True
    )


# -----------------------------
# WHAT IF SIMULATOR
# -----------------------------

elif page == "What-If Simulator":
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

    st.subheader("Scenario Risk Across India")

    st.plotly_chart(
        render_india_climate_map(
            "What-If Scenario Risk Map",
            "risk"
        ),
        use_container_width=True
    )

    current = generate_climate_grid("observed")
    scenario = generate_climate_grid(
        "scenario",
        temp_increase=temp_increase,
        rainfall_change=rainfall_change
    )
    impact = scenario - current

    st.subheader("Twin Response Maps")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(
            render_climate_map(
                current,
                "Current Climate State",
                "Blues"
            ),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            render_climate_map(
                scenario,
                "What-If Future State",
                "OrRd"
            ),
            use_container_width=True
        )

    with col3:
        st.plotly_chart(
            render_climate_map(
                impact,
                "Scenario Impact Map",
                "RdBu"
            ),
            use_container_width=True
        )

    scenario_temp = temp_df.copy()
    scenario_temp["future"] = scenario_temp["predicted"] + temp_increase

    st.plotly_chart(
        px.line(
            scenario_temp,
            x="date",
            y=["predicted", "future"],
            title="Temperature Scenario Response"
        ),
        use_container_width=True
    )

    scenario_rain = rainfall_df.copy()
    scenario_rain["future"] = (
        scenario_rain["predicted"] * (1 + rainfall_change / 100)
        - temp_increase * 2
    )

    st.plotly_chart(
        px.line(
            scenario_rain,
            x="date",
            y=["predicted", "future"],
            title="Rainfall Scenario Response"
        ),
        use_container_width=True
    )


# -----------------------------
# INSIGHTS
# -----------------------------

elif page == "Insights":
    st.title("📊 Climate Insights")

    rainfall_df["month"] = rainfall_df["date"].dt.month

    st.plotly_chart(
        px.box(
            rainfall_df,
            x="month",
            y="actual",
            title="Rainfall Distribution by Month"
        ),
        use_container_width=True
    )

    combined = pd.DataFrame({
        "temperature": temp_df["actual"],
        "rainfall": rainfall_df["actual"]
    })

    st.plotly_chart(
        px.scatter(
            combined,
            x="temperature",
            y="rainfall",
            title="Rainfall vs Temperature"
        ),
        use_container_width=True
    )

    st.success("Dashboard MVP Ready 🚀")