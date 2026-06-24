import streamlit as st


def show_metrics():
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("RMSE", "2.84")
    col2.metric("MAE", "1.91")
    col3.metric("Skill Score", "0.18")
    col4.metric("Correlation", "0.67")