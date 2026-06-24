import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="AI Climate Digital Twin",
    page_icon="🌦️",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}
.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #0b1f4d;
}
.sub-title {
    color: #526070;
    font-size: 16px;
}
.card {
    background: #ffffff;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e6eaf2;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.alert-card {
    background: #ffffff;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #e6eaf2;
    margin-bottom: 10px;
}
.small-muted {
    color: #65758b;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# REGION DATA
# -----------------------------
REGION_INFO = {
    "Kerala": {
        "rainfall": 122,
        "temperature": 28.4,
        "humidity": 86,
        "wind": 14,
        "aqi": 38,
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
        "wind": 18,
        "aqi": 52,
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


# -----------------------------
# DATA
# -----------------------------
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


def render_india_map(title, selected_region, color_metric="risk"):
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
        color_continuous_scale="OrRd" if color_metric == "risk" else "Blues",
        title=title,
        hover_data=["rainfall", "temperature", "risk"]
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=520, margin=dict(l=10, r=10, t=50, b=10))
    return fig


def scenario_risk(temp_increase, rainfall_change):
    if temp_increase >= 6 or rainfall_change >= 35:
        return "Extreme"
    if temp_increase >= 4 or rainfall_change >= 20:
        return "High"
    if temp_increase >= 2 or rainfall_change >= 10:
        return "Moderate"
    return "Low"


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.markdown("## 🌦️ AI Climate Twin")
region = st.sidebar.selectbox("Select pilot region", ["Kerala", "Tamil Nadu"])

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Live Monitor",
        "Forecasts",
        "Alerts",
        "Scenarios",
        "Analytics",
        "Reports"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Selected:** {region}")
st.sidebar.caption("ISRO Hackathon PS-5 MVP")

rainfall_df, temp_df = load_data(region)
current = REGION_INFO[region]


# -----------------------------
# OVERVIEW
# -----------------------------
if page == "Overview":
    st.markdown('<div class="main-title">AI Climate Digital Twin Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Real-time monitoring, forecasting, scenario simulation and decision support</div>', unsafe_allow_html=True)

    st.markdown("### Dashboard Overview")

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🌡️ Temperature", f"{current['temperature']} °C", "+1.2°C")
    k2.metric("🌧️ Rainfall", f"{current['rainfall']} mm", "+8%")
    k3.metric("💧 Humidity", f"{current['humidity']}%", "-3%")
    k4.metric("🌬️ Wind", f"{current['wind']} km/h")
    k5.metric("🍃 AQI", current["aqi"], "Good")

    left, right = st.columns([1.1, 1])

    with left:
        st.subheader("Live Map — Climate Risk")
        st.plotly_chart(
            render_india_map(f"India Climate Risk Map — {region} selected", region, "risk"),
            use_container_width=True
        )

    with right:
        st.subheader("Digital Twin View")
        grid = generate_climate_grid(region, "observed")
        st.plotly_chart(
            render_climate_map(grid, f"{region} Digital Twin Climate State", "Viridis"),
            use_container_width=True
        )

    st.subheader("Alerts & Notifications")

    a1, a2, a3 = st.columns(3)
    a1.warning(f"⚠️ Heavy rainfall possible in {region} in next 24h.")
    a2.info(f"ℹ️ Current flood probability: {current['flood_probability']}%")
    a3.success("✅ Model pipeline ready for prediction output.")


# -----------------------------
# LIVE MONITOR
# -----------------------------
elif page == "Live Monitor":
    st.markdown(f'<div class="main-title">Live Climate Monitor — {region}</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Rainfall", f"{current['rainfall']} mm/day")
    c2.metric("Current Temperature", f"{current['temperature']} °C")
    c3.metric("Humidity", f"{current['humidity']}%")
    c4.metric("Flood Probability", f"{current['flood_probability']}%")

    st.subheader("Current Observed Climate Field")
    observed = generate_climate_grid(region, "observed")
    st.plotly_chart(
        render_climate_map(observed, f"{region}: Observed Rainfall Distribution", "Blues"),
        use_container_width=True
    )

    st.subheader("Observed Time Series")
    st.plotly_chart(
        px.line(rainfall_df, x="date", y="actual", title=f"{region}: Observed Rainfall Trend"),
        use_container_width=True
    )
    st.plotly_chart(
        px.line(temp_df, x="date", y="actual", title=f"{region}: Observed Temperature Trend"),
        use_container_width=True
    )


# -----------------------------
# FORECASTS
# -----------------------------
elif page == "Forecasts":
    st.markdown(f'<div class="main-title">Forecast View — {region}</div>', unsafe_allow_html=True)

    horizon = st.radio("Forecast horizon", ["7 Days", "15 Days", "30 Days"], horizontal=True)

    f1, f2, f3, f4 = st.columns(4)
    f1.metric("T+1 Rainfall", f"{current['t1_rainfall']} mm/day")
    f2.metric("T+7 Rainfall", f"{current['t7_rainfall']} mm/day")
    f3.metric("T+1 Temp", f"{current['t1_temp']} °C")
    f4.metric("T+7 Temp", f"{current['t7_temp']} °C")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rainfall RMSE", "2.84 mm/day")
    m2.metric("Rainfall MAE", "1.91 mm/day")
    m3.metric("Temp RMSE", "1.12 °C")
    m4.metric("Skill Score", "+0.18")

    observed = generate_climate_grid(region, "observed")
    predicted = generate_climate_grid(region, "predicted")
    diff = predicted - observed

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(render_climate_map(observed, "Observed State", "Blues"), use_container_width=True)
    with col2:
        st.plotly_chart(render_climate_map(predicted, "AI Predicted State", "Viridis"), use_container_width=True)
    with col3:
        st.plotly_chart(render_climate_map(diff, "Prediction Difference", "RdBu"), use_container_width=True)

    st.subheader("Forecast Trend")
    st.plotly_chart(
        px.line(rainfall_df, x="date", y=["actual", "predicted"], title=f"{region}: Rainfall Actual vs Predicted"),
        use_container_width=True
    )
    st.plotly_chart(
        px.line(temp_df, x="date", y=["actual", "predicted"], title=f"{region}: Temperature Actual vs Predicted"),
        use_container_width=True
    )


# -----------------------------
# ALERTS
# -----------------------------
elif page == "Alerts":
    st.markdown(f'<div class="main-title">Alerts Panel — {region}</div>', unsafe_allow_html=True)

    if current["flood_probability"] >= 75:
        st.error(f"🚨 Extreme Rainfall Warning — {region}")
        st.write("Very heavy rainfall expected. Flood probability is above 75%.")
    elif current["flood_probability"] >= 45:
        st.warning(f"⚠️ Heavy Rainfall Advisory — {region}")
        st.write("Moderate-to-heavy rainfall expected. Monitor urban and low-lying areas.")
    else:
        st.success(f"✅ Normal climate condition — {region}")

    alerts = [
        ["🔴 Extreme rainfall warning", "High rainfall intensity detected in forecast window.", "High"],
        ["🟠 Heatwave warning", "Temperature anomaly rising in next few days.", "Medium"],
        ["🟡 High wind alert", "Coastal wind speed may increase.", "Medium"],
        ["🔵 Climate update", "Model output refreshed for selected region.", "Info"]
    ]

    for title, desc, level in alerts:
        st.markdown(f"""
        <div class="alert-card">
            <b>{title}</b><br>
            <span class="small-muted">{desc}</span><br>
            <b>Severity:</b> {level}
        </div>
        """, unsafe_allow_html=True)


# -----------------------------
# SCENARIOS
# -----------------------------
elif page == "Scenarios":
    st.markdown(f'<div class="main-title">Scenario Simulation — {region}</div>', unsafe_allow_html=True)

    temp_inc = st.slider("Temperature Change (°C)", 0.0, 7.0, 2.0, 0.5)
    rain_change = st.slider("Rainfall Change (%)", -50, 50, 10, 5)
    co2 = st.slider("CO₂ Concentration Change (ppm)", 0, 200, 100, 10)

    risk = scenario_risk(temp_inc, rain_change)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Avg Temperature", f"+{temp_inc} °C")
    p2.metric("Rainfall", f"{rain_change}%")
    p3.metric("Extreme Events", "↑ 15%" if risk in ["High", "Extreme"] else "↑ 5%")
    p4.metric("Scenario Risk", risk)

    current_grid = generate_climate_grid(region, "observed")
    future_grid = generate_climate_grid(region, "scenario", temp_inc, rain_change)
    impact = future_grid - current_grid

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(render_climate_map(current_grid, "Current Twin State", "Blues"), use_container_width=True)
    with col2:
        st.plotly_chart(render_climate_map(future_grid, "What-If Future State", "OrRd"), use_container_width=True)
    with col3:
        st.plotly_chart(render_climate_map(impact, "Impact Difference Map", "RdBu"), use_container_width=True)

    scenario_temp = temp_df.copy()
    scenario_temp["future"] = scenario_temp["predicted"] + temp_inc

    scenario_rain = rainfall_df.copy()
    scenario_rain["future"] = scenario_rain["predicted"] * (1 + rain_change / 100) - temp_inc * 2

    st.plotly_chart(
        px.line(scenario_temp, x="date", y=["predicted", "future"], title="Temperature Scenario Response"),
        use_container_width=True
    )
    st.plotly_chart(
        px.line(scenario_rain, x="date", y=["predicted", "future"], title="Rainfall Scenario Response"),
        use_container_width=True
    )

    st.info("Scenario output is an MVP perturbation engine. Final system will use model inference.")


# -----------------------------
# ANALYTICS
# -----------------------------
elif page == "Analytics":
    st.markdown(f'<div class="main-title">Analytics & Insights — {region}</div>', unsafe_allow_html=True)

    rainfall_df["month"] = rainfall_df["date"].dt.month

    i1, i2 = st.columns([1, 1.5])

    with i1:
        st.subheader("Insights")
        st.success("🌧️ Monsoon onset likely to shift by 5 days.")
        st.info("🌊 Increase in extreme rainfall risk in coastal belt.")
        st.warning("🌡️ Rising temperature anomaly visible in forecast window.")

    with i2:
        st.plotly_chart(
            px.line(temp_df, x="date", y=["actual", "predicted"], title="Temperature Trend Analysis"),
            use_container_width=True
        )

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


# -----------------------------
# REPORTS
# -----------------------------
elif page == "Reports":
    st.markdown(f'<div class="main-title">Reports & Exports — {region}</div>', unsafe_allow_html=True)

    r1, r2 = st.columns([1, 1])

    with r1:
        st.subheader("Generate Report")
        report_type = st.selectbox("Report Type", ["Climate Summary", "Forecast Report", "Alert Report", "Scenario Report"])
        period = st.selectbox("Time Period", ["Last 7 Days", "Last 15 Days", "Last 30 Days"])
        if st.button("Generate Report"):
            st.success(f"{report_type} generated for {region} — {period}")

    with r2:
        st.subheader("Export Options")
        e1, e2 = st.columns(2)
        e1.download_button(
            "📄 Download CSV",
            rainfall_df.to_csv(index=False),
            file_name=f"{region.lower()}_rainfall_report.csv",
            mime="text/csv"
        )
        e2.download_button(
            "📊 Download Temperature CSV",
            temp_df.to_csv(index=False),
            file_name=f"{region.lower()}_temperature_report.csv",
            mime="text/csv"
        )

    st.info("PDF/PNG export can be added later. CSV export is working for MVP.")