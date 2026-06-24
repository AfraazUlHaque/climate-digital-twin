import streamlit as st
from dashboard.components.maps import render_map

def render():

    st.title(
        "🌦️ AI-Powered Digital Twin of India's Climate"
    )

    st.write(
        "ISRO Hackathon PS-5"
    )

    render_map()