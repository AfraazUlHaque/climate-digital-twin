import plotly.express as px


def rainfall_chart(df):
    fig = px.line(
        df,
        x="date",
        y=["actual", "predicted"],
        title="Rainfall Forecast"
    )
    return fig


def temperature_chart(df):
    fig = px.line(
        df,
        x="date",
        y=["actual", "predicted"],
        title="Temperature Forecast"
    )
    return fig