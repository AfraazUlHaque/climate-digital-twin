import plotly.express as px


def rainfall_forecast_chart(rainfall_df):
    fig = px.line(
        rainfall_df,
        x="date",
        y=["actual", "predicted"],
        title="Rainfall: Actual vs Predicted",
        labels={
            "value": "Rainfall (mm/day)",
            "date": "Date",
            "variable": "Series"
        }
    )
    return fig


def temperature_forecast_chart(temp_df):
    fig = px.line(
        temp_df,
        x="date",
        y=["actual", "predicted"],
        title="Temperature: Actual vs Predicted",
        labels={
            "value": "Temperature (°C)",
            "date": "Date",
            "variable": "Series"
        }
    )
    return fig


def observed_rainfall_chart(rainfall_df):
    fig = px.line(
        rainfall_df,
        x="date",
        y="actual",
        title="Observed Rainfall Trend",
        labels={
            "actual": "Rainfall (mm/day)",
            "date": "Date"
        }
    )
    return fig


def observed_temperature_chart(temp_df):
    fig = px.line(
        temp_df,
        x="date",
        y="actual",
        title="Observed Temperature Trend",
        labels={
            "actual": "Temperature (°C)",
            "date": "Date"
        }
    )
    return fig


def scenario_temperature_chart(scenario_df):
    fig = px.line(
        scenario_df,
        x="date",
        y=["predicted", "future"],
        title="Temperature Scenario Simulation",
        labels={
            "value": "Temperature (°C)",
            "date": "Date",
            "variable": "Series"
        }
    )
    return fig


def rainfall_temperature_scatter(temp_df, rainfall_df):
    fig = px.scatter(
        x=temp_df["actual"],
        y=rainfall_df["actual"],
        labels={
            "x": "Temperature (°C)",
            "y": "Rainfall (mm/day)"
        },
        title="Rainfall vs Temperature Relationship"
    )
    return fig