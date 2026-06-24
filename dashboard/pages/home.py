import streamlit as st

from components.maps import (
    generate_climate_grid,
    render_climate_map
)


def render():
    st.title("🌦️ AI-Powered Digital Twin of India's Climate")

    st.markdown("""
    ### Bharatiya Antariksh Hackathon 2026 | ISRO / NRSC | PS-5

    This dashboard demonstrates a prototype **Climate Digital Twin** for India using:

    - Current climate state representation
    - AI-based rainfall and temperature prediction
    - What-if climate scenario simulation
    - Interactive visual analytics
    """)

    col1, col2, col3 = st.columns(3)

    col1.metric("Pilot Region", "Kerala + Tamil Nadu")
    col2.metric("Forecast Horizon", "T+1 / T+7")
    col3.metric("Core Model", "ConvLSTM")

    st.markdown("---")

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

    st.subheader("Prototype Climate State Preview")

    grid = generate_climate_grid("observed")

    st.plotly_chart(
        render_climate_map(
            grid,
            "Observed Climate State Preview",
            "Blues"
        ),
        use_container_width=True
    )

    st.success("Dashboard MVP deployed successfully.")