import streamlit as st
import plotly.express as px

from dashboard.utils.data_loader import load_data

def render():

    rainfall_df, temp_df = load_data()

    st.title("📊 Insights")

    combined = {
        "temperature": temp_df["actual"],
        "rainfall": rainfall_df["actual"]
    }

    fig = px.scatter(
        combined,
        x="temperature",
        y="rainfall"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )