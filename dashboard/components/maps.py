import numpy as np
import plotly.express as px


def generate_climate_grid(mode="observed", temp_increase=0, rainfall_change=0):
    np.random.seed(42)

    base = np.random.normal(loc=65, scale=18, size=(25, 25))
    base = np.clip(base, 0, 140)

    if mode == "predicted":
        grid = base + np.random.normal(3, 8, size=(25, 25))

    elif mode == "scenario":
        grid = base * (1 + rainfall_change / 100) - (temp_increase * 3)

    elif mode == "difference":
        predicted = base + np.random.normal(3, 8, size=(25, 25))
        grid = predicted - base

    else:
        grid = base

    return np.clip(grid, -50, 160)


def render_climate_map(grid, title, color_scale="Blues"):
    fig = px.imshow(
        grid,
        color_continuous_scale=color_scale,
        title=title,
        labels=dict(color="Rainfall mm/day")
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig

def render_map():
    import streamlit as st

    grid = generate_climate_grid("observed")

    fig = render_climate_map(
        grid,
        "Current Climate State",
        "Blues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )