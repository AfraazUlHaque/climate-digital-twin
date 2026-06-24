import streamlit as st
import plotly.express as px

from dashboard.utils.data_loader import load_data

def render():

    rainfall_df, temp_df = load_data()

    st.title("🔮 Predictions")

    st.metric(
        "Rainfall RMSE",
        "2.84"
    )

    fig = px.line(
        rainfall_df,
        x="date",
        y=["actual", "predicted"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )