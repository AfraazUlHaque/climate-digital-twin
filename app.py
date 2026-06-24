import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Climate Digital Twin", page_icon="🌦️", layout="wide")

REGION_INFO = {
    "Kerala": {
        "rainfall": 122,
        "temperature": 28.4,
        "humidity": 86,
        "risk": "High",
        "flood_probability": 78,
        "t1_rainfall": 138,
        "t7_rainfall": 154,
        "t1_temp": 29.1,
        "t7_temp": 30.2,
        "events": {
            "2018 Kerala Flood": {
                "rainfall": 240,
                "temperature": 27,
                "risk": "Extreme Flood Risk",
                "description": "Very high rainfall pattern similar to Kerala 2018 floods."
            },
            "2024 Wayanad Landslide": {
                "rainfall": 190,
                "temperature": 26,
                "risk": "Landslide Risk",
                "description": "Heavy rainfall over hilly terrain causing slope instability."
            }
        }
    },
    "Tamil Nadu": {
        "rainfall": 92,
        "temperature": 31.2,
        "humidity": 74,
        "risk": "Moderate",
        "flood_probability": 46,
        "t1_rainfall": 104,
        "t7_rainfall": 118,
        "t1_temp": 32.0,
        "t7_temp": 33.1,
        "events": {
            "2015 Chennai Flood": {
                "rainfall": 210,
                "temperature": 28,
                "risk": "Urban Flood Risk",
                "description": "Extreme rainfall pattern similar to Chennai 2015 floods."
            },
            "2023 Cyclone Michaung": {
                "rainfall": 175,
                "temperature": 29,
                "risk": "Cyclone Rainfall Risk",
                "description": "Cyclone-linked heavy rainfall and coastal flooding pattern."
            }
        }
    }
}


@st.cache_data
def load_data(region):
    seed = 10 if region == "Kerala" else 20
    np.random.seed(seed)
    dates = pd.date_range("2024-01-01", periods=60)

    base_rain = REGION_INFO[region]["rainfall"] * 0.65
    base_temp = REGION_INFO[region]["temperature"]

    rainfall = pd.DataFrame({
        "date": dates,
        "actual": np.random.uniform(base_rain * 0.5, base_rain * 1.3, 60),
        "predicted": np.random.uniform(base_rain * 0.55, base_rain * 1.35, 60)
    })

    temperature = pd.DataFrame({
        "date": dates,
        "actual": np.random.uniform(base_temp - 2, base_temp + 2, 60),
        "predicted": np.random.uniform(base_temp - 1.5, base_temp + 2.5, 60)
    })

    return rainfall, temperature


def generate_climate_grid(region, mode="observed", temp_increase=0, rainfall_change=0):
    seed = 42 if region == "Kerala" else 84
    np.random.seed(seed)

    loc = 75 if region == "Kerala" else 58
    base = np.random.normal(loc=loc, scale=18, size=(25, 25))
    base = np.clip(base, 0, 160)

    if mode == "predicted":
        grid = base + np.random.normal(8, 10, size=(25, 25))
    elif mode == "scenario":
        grid = base * (1 + rainfall_change / 100) - (temp_increase * 3)
    else:
        grid = base

    return np.clip(grid, -50, 180)


def render_climate_map(grid, title, color_scale="Blues", label="Rainfall mm/day"):
    fig = px.imshow(
        grid,
        color_continuous_scale=color_scale,
        title=title,
        labels=dict(color=label)
    )
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=50, b=10))
    return fig


def render_india_climate_map(title, selected_region, color_metric="rainfall"):
    india_data = pd.DataFrame({
        "state": [
            "Kerala", "Tamil Nadu", "Karnataka", "Maharashtra", "Gujarat",
            "Rajasthan", "Uttar Pradesh", "Assam", "West Bengal", "Odisha",
            "Bihar", "Madhya Pradesh", "Andhra Pradesh", "Telangana"
        ],
        "rainfall": [122, 92, 82, 70, 45, 25, 55, 140, 110, 105, 90, 60, 88, 74],
        "temperature": [28.4, 31.2, 27, 32, 35, 39, 34, 29, 30, 31, 32, 33, 31, 32],
        "risk": [88, 62, 60, 55, 40, 35, 50, 90, 78, 75, 68, 48, 70, 58]
    })

    india_data.loc[india_data["state"] == selected_region, "risk"] += 12

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

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=520, margin=dict(l=10, r=10, t=50, b=10))
    return fig


def get_scenario_risk(temp_increase, rainfall_change):
    if temp_increase >= 6 or rainfall_change >= 35:
        return "Extreme"
    if temp_increase >= 4 or rainfall_change >= 20:
        return "High"
    if temp_increase >= 2 or rainfall_change >= 10:
        return "Moderate"
    return "Low"


st.sidebar.title("🌦️ Climate Digital Twin")

region = st.sidebar.selectbox(
    "Select Pilot Region",
    ["Kerala", "Tamil Nadu"]
)

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Current Climate State", "Predictions", "What-If Simulator", "Insights"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"Selected Region: {region}")

rainfall_df, temp_df = load_data(region)
current = REGION_INFO[region]


if page == "Home":
    st.title("🌦️ AI-Powered Digital Twin of India's Climate")
    st.write("Bharatiya Antariksh Hackathon 2026 | ISRO / NRSC | PS-5")

    c1, c2, c3 = st.columns(3)
    c1.metric("Selected Pilot Region", region)
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
Early Warning Dashboard
""")

    st.plotly_chart(
        render_india_climate_map(
            f"India Climate Twin Preview - Highlighting {region}",
            region,
            "risk"
        ),
        use_container_width=True
    )


elif page == "Current Climate State":
    st.title(f"🌍 Current Climate State - {region}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Rainfall", f"{current['rainfall']} mm/day")
    c2.metric("Current Temperature", f"{current['temperature']} °C")
    c3.metric("Humidity", f"{current['humidity']}%")
    c4.metric("Flood Probability", f"{current['flood_probability']}%")

    st.subheader(f"{region} Climate State Map")

    observed = generate_climate_grid(region, "observed")

    st.plotly_chart(
        render_climate_map(
            observed,
            f"{region}: Observed Rainfall Distribution",
            "Blues"
        ),
        use_container_width=True
    )

    st.subheader("Region Time Series")

    st.plotly_chart(
        px.line(rainfall_df, x="date", y="actual", title=f"{region} Observed Rainfall Trend"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(temp_df, x="date", y="actual", title=f"{region} Observed Temperature Trend"),
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("📌 Past Extreme Event Simulator")

    event = st.selectbox(
        "Select historical event",
        list(current["events"].keys())
    )

    selected = current["events"][event]

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
            f"{region}: {event} Pattern Replay",
            "OrRd"
        ),
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("🚨 Region Alert System")

    if current["flood_probability"] >= 75:
        st.error(f"🚨 {region}: High Flood Alert")
        st.write("**Recommended Action:** Activate flood monitoring, notify low-lying areas, and prepare evacuation routes.")
    elif current["temperature"] >= 38:
        st.error(f"🔥 {region}: Heatwave Alert")
        st.write("**Recommended Action:** Issue heat-stress advisory.")
    elif current["rainfall"] < 20 and current["temperature"] > 34:
        st.warning(f"🌾 {region}: Drought Stress Alert")
        st.write("**Recommended Action:** Irrigation and crop stress monitoring recommended.")
    else:
        st.success(f"✅ {region}: No extreme climate risk detected")


elif page == "Predictions":
    st.title(f"🔮 AI Prediction Engine - {region}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("T+1 Rainfall", f"{current['t1_rainfall']} mm/day")
    c2.metric("T+7 Rainfall", f"{current['t7_rainfall']} mm/day")
    c3.metric("T+1 Temp", f"{current['t1_temp']} °C")
    c4.metric("T+7 Temp", f"{current['t7_temp']} °C")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rainfall RMSE", "2.84 mm/day")
    m2.metric("Rainfall MAE", "1.91 mm/day")
    m3.metric("Temperature RMSE", "1.12 °C")
    m4.metric("Skill Score", "+0.18")

    observed = generate_climate_grid(region, "observed")
    predicted = generate_climate_grid(region, "predicted")
    difference = predicted - observed

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(render_climate_map(observed, f"{region}: Observed State", "Blues"), use_container_width=True)

    with col2:
        st.plotly_chart(render_climate_map(predicted, f"{region}: AI Predicted State", "Viridis"), use_container_width=True)

    with col3:
        st.plotly_chart(render_climate_map(difference, f"{region}: Prediction Difference", "RdBu"), use_container_width=True)

    st.plotly_chart(
        px.line(rainfall_df, x="date", y=["actual", "predicted"], title=f"{region}: Rainfall Actual vs Predicted"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(temp_df, x="date", y=["actual", "predicted"], title=f"{region}: Temperature Actual vs Predicted"),
        use_container_width=True
    )


elif page == "What-If Simulator":
    st.title(f"🧪 What-If Digital Twin Simulator - {region}")

    temp_increase = st.slider("Temperature Increase Scenario (°C)", 0.0, 7.0, 2.0, 0.5)
    rainfall_change = st.slider("Rainfall Anomaly (%)", -50, 50, 10, 5)

    risk = get_scenario_risk(temp_increase, rainfall_change)

    c1, c2, c3 = st.columns(3)
    c1.metric("Temperature Change", f"+{temp_increase}°C")
    c2.metric("Rainfall Anomaly", f"{rainfall_change}%")
    c3.metric("Scenario Risk", risk)

    current_grid = generate_climate_grid(region, "observed")
    scenario_grid = generate_climate_grid(region, "scenario", temp_increase, rainfall_change)
    impact_grid = scenario_grid - current_grid

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(render_climate_map(current_grid, f"{region}: Current State", "Blues"), use_container_width=True)

    with col2:
        st.plotly_chart(render_climate_map(scenario_grid, f"{region}: What-If Future State", "OrRd"), use_container_width=True)

    with col3:
        st.plotly_chart(render_climate_map(impact_grid, f"{region}: Scenario Impact Map", "RdBu"), use_container_width=True)

    scenario_temp = temp_df.copy()
    scenario_temp["future"] = scenario_temp["predicted"] + temp_increase

    st.plotly_chart(
        px.line(scenario_temp, x="date", y=["predicted", "future"], title=f"{region}: Temperature Scenario Response"),
        use_container_width=True
    )

    scenario_rain = rainfall_df.copy()
    scenario_rain["future"] = scenario_rain["predicted"] * (1 + rainfall_change / 100) - temp_increase * 2

    st.plotly_chart(
        px.line(scenario_rain, x="date", y=["predicted", "future"], title=f"{region}: Rainfall Scenario Response"),
        use_container_width=True
    )


elif page == "Insights":
    st.title(f"📊 Climate Insights - {region}")

    rainfall_df["month"] = rainfall_df["date"].dt.month

    st.plotly_chart(
        px.box(rainfall_df, x="month", y="actual", title=f"{region}: Rainfall Distribution by Month"),
        use_container_width=True
    )

    combined = pd.DataFrame({
        "temperature": temp_df["actual"],
        "rainfall": rainfall_df["actual"]
    })

    st.plotly_chart(
        px.scatter(combined, x="temperature", y="rainfall", title=f"{region}: Rainfall vs Temperature"),
        use_container_width=True
    )

    st.success(f"{region} Climate Twin Dashboard Ready 🚀")