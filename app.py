import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Climate Digital Twin",
    page_icon="🌍",
    layout="wide"
)

# ---------------- DATA ----------------
np.random.seed(42)

dates = pd.date_range("2026-01-01", periods=30)

forecast_df = pd.DataFrame({
    "Date": dates,
    "Temperature": np.random.uniform(25, 36, 30),
    "Rainfall": np.random.uniform(0, 80, 30),
    "Humidity": np.random.uniform(45, 90, 30),
    "Wind Speed": np.random.uniform(5, 25, 30)
})

cities = pd.DataFrame({
    "City": ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru", "Hyderabad"],
    "lat": [28.61, 19.07, 13.08, 22.57, 12.97, 17.38],
    "lon": [77.20, 72.87, 80.27, 88.36, 77.59, 78.48],
    "Risk": [75, 55, 80, 65, 40, 50],
    "Rainfall": [22, 45, 78, 60, 18, 30]
})

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 AI Climate Digital Twin")
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Live Monitor", "Forecasts", "Alerts", "Scenario Simulation", "Reports"]
)

st.sidebar.markdown("---")
st.sidebar.metric("Location", "India")
st.sidebar.metric("Last Updated", "10:30 AM")

# ---------------- OVERVIEW ----------------
if page == "Overview":
    st.title("Dashboard Overview")
    st.caption("Real-time Climate Monitoring, Forecasting & Decision Support")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Temperature", "32.6 °C", "+1.2 °C")
    c2.metric("Rainfall 24h", "12.8 mm", "+8%")
    c3.metric("Humidity", "67%", "-3%")
    c4.metric("Wind Speed", "12 km/h", "Stable")
    c5.metric("AQI", "42", "Good")

    st.markdown("### Live Climate Map")
    fig_map = px.scatter_mapbox(
        cities,
        lat="lat",
        lon="lon",
        size="Risk",
        color="Rainfall",
        hover_name="City",
        zoom=3.5,
        height=420,
        mapbox_style="carto-positron",
        title="Rainfall & Risk Intensity"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Temperature Trend")
        fig = px.line(forecast_df, x="Date", y="Temperature", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Rainfall Trend")
        fig = px.bar(forecast_df, x="Date", y="Rainfall")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Alerts & Notifications")
    st.warning("⚠️ Heavy rainfall predicted in Maharashtra in next 24 hours.")
    st.error("🚨 Heatwave conditions likely in Rajasthan.")
    st.info("ℹ️ Normal conditions across South India.")

# ---------------- LIVE MONITOR ----------------
elif page == "Live Monitor":
    st.title("Live Climate Monitor")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Live Weather Parameters")
        st.metric("Temperature", "31.8 °C")
        st.metric("Pressure", "1012 hPa")
        st.metric("Cloud Cover", "62%")
        st.metric("Soil Moisture", "38%")

    with col2:
        st.subheader("Digital Twin View")
        st.image(
            "https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4",
            caption="Virtual climate representation",
            use_container_width=True
        )

# ---------------- FORECASTS ----------------
elif page == "Forecasts":
    st.title("Forecast View")

    days = st.selectbox("Select Forecast Range", ["7 Days", "15 Days", "30 Days"])

    st.markdown("### Weather Forecast")
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=forecast_df["Temperature"],
        mode="lines+markers",
        name="Temperature"
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["Date"],
        y=forecast_df["Humidity"],
        mode="lines+markers",
        name="Humidity"
    ))

    fig.add_trace(go.Bar(
        x=forecast_df["Date"],
        y=forecast_df["Rainfall"],
        name="Rainfall",
        opacity=0.5
    ))

    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- ALERTS ----------------
elif page == "Alerts":
    st.title("Alerts Panel")

    alerts = [
        ["Extreme Rainfall Warning", "Very heavy rainfall expected in Konkan & Goa region.", "High"],
        ["Heatwave Warning", "Heatwave conditions likely in Rajasthan for next 2 days.", "High"],
        ["High Wind Alert", "Strong surface winds expected in coastal Gujarat.", "Medium"],
        ["Air Quality Update", "Air quality is moderate in Delhi NCR.", "Low"]
    ]

    df_alerts = pd.DataFrame(alerts, columns=["Alert", "Description", "Severity"])
    st.dataframe(df_alerts, use_container_width=True)

# ---------------- SCENARIO ----------------
elif page == "Scenario Simulation":
    st.title("Scenario Simulation: What-If Analysis")

    temp_change = st.slider("Temperature Increase (°C)", 0, 5, 2)
    rainfall_change = st.slider("Rainfall Change (%)", -50, 50, -10)
    co2_change = st.slider("CO₂ Increase (ppm)", 0, 300, 100)

    st.markdown("### Projected Impact")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Temperature", f"+{temp_change * 1.1:.1f} °C")
    c2.metric("Rainfall", f"{rainfall_change}%")
    c3.metric("Extreme Events", f"+{temp_change * 7}%")
    c4.metric("Agricultural Yield", f"{-abs(rainfall_change)//2}%")

    impact = pd.DataFrame({
        "Factor": ["Temperature", "Rainfall", "Extreme Events", "Crop Yield"],
        "Impact": [temp_change * 20, rainfall_change, temp_change * 15, -abs(rainfall_change)]
    })

    fig = px.bar(impact, x="Factor", y="Impact", title="Scenario Impact Analysis")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- REPORTS ----------------
elif page == "Reports":
    st.title("Reports & Exports")

    report_type = st.selectbox(
        "Select Report Type",
        ["Climate Summary", "Rainfall Forecast", "Extreme Weather Risk", "Agriculture Advisory"]
    )

    region = st.selectbox(
        "Select Region",
        ["India", "Maharashtra", "Delhi NCR", "Assam", "Tamil Nadu", "Rajasthan"]
    )

    time_period = st.selectbox(
        "Time Period",
        ["7 Days", "15 Days", "30 Days", "Seasonal"]
    )

    if st.button("Generate Report"):
        st.success("Report generated successfully!")

        st.markdown(f"""
        ### {report_type} Report
        
        **Region:** {region}  
        **Time Period:** {time_period}
        
        **Key Insights:**
        - Rainfall variability is increasing.
        - Temperature trend shows gradual rise.
        - Some regions show higher risk of extreme events.
        - AI model recommends continuous monitoring.
        """)

        st.download_button(
            "Download CSV",
            forecast_df.to_csv(index=False),
            "climate_report.csv",
            "text/csv"
        )