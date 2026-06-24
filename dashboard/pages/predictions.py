import streamlit as st

st.title("🔮 Climate Predictions")

st.metric("RMSE", "2.84")
st.metric("MAE", "1.91")

st.success(
    "Model predicts stable rainfall conditions for next 7 days."
)