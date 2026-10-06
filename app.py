import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("predictions_2023.csv")
HOUR_BUCKET_MAP = {0: "Night (00-05)", 1: "Morning (06-11)", 2: "Afternoon (12-17)", 3: "Evening (18-23)"}
DAY_OF_WEEK_MAP = {1: "Sunday", 2: "Monday", 3: "Tuesday", 4: "Wednesday", 5: "Thursday", 6: "Friday", 7: "Saturday"}

df["hour_bucket_label"] = df["hour_bucket"].astype(int).map(HOUR_BUCKET_MAP)
df["day_of_week_label"] = df["day_of_week"].astype(int).map(DAY_OF_WEEK_MAP)
df["area"] = df["area"].astype(str)

divisions = sorted(df["area"].unique().tolist())
hour_buckets = list(HOUR_BUCKET_MAP.values())
day_names = list(DAY_OF_WEEK_MAP.values())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    html.H2("LAPD Crime Prediction Dashboard", className="my-3 text-primary fw-bold"),
    dbc.Row([
        dbc.Col([html.Label("LAPD Division:"), dcc.Dropdown(id="division-filter", options=[{"label": "All Divisions", "value": "ALL"}] + [{"label": d, "value": d} for d in divisions], value="ALL", clearable=False)], md=4),
        dbc.Col([html.Label("Hour Bucket:"), dcc.Dropdown(id="hour-bucket-filter", options=[{"label": "All Hours", "value": "ALL"}] + [{"label": h, "value": h} for h in hour_buckets], value="ALL", clearable=False)], md=4),
        dbc.Col([html.Label("Day of Week:"), dcc.Dropdown(id="day-filter", options=[{"label": "All Days", "value": "ALL"}] + [{"label": d, "value": d} for d in day_names], value="ALL", clearable=False)], md=4),
    ], className="mb-4"),
    dbc.Card([
        dbc.CardBody([
            html.H5("Filtered Subset MAE", className="text-muted fs-6"),
            html.H2(id="mae-card", className="text-primary fw-bold")
        ])
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([dcc.Graph(id="line-chart")], md=6),
        dbc.Col([dcc.Graph(id="bar-chart")], md=6)
    ])
], fluid=True)

@app.callback(
    [Output("mae-card", "children"), Output("line-chart", "figure"), Output("bar-chart", "figure")],
    [Input("division-filter", "value"), Input("hour-bucket-filter", "value"), Input("day-filter", "value")]
)
def update_graphs(div, hour, day):
    dff = df.copy()
    if div and div != "ALL":
        dff = dff[dff["area"] == str(div)]
    if hour and hour != "ALL":
        dff = dff[dff["hour_bucket_label"] == hour]
    if day and day != "ALL":
        dff = dff[dff["day_of_week_label"] == day]

    mae_str = f"{mean_absolute_error(dff['actual'], dff['predicted']):.2f} crimes / slice" if len(dff) > 0 else "N/A"
    m_agg = dff.groupby("month")[["actual", "predicted"]].sum().reset_index()
    fig_line = px.line(m_agg, x="month", y=["actual", "predicted"], title="Monthly Crimes (Actual vs Predicted)", markers=True)
    h_agg = dff.groupby("hour_bucket_label")[["actual", "predicted"]].mean().reset_index()
    fig_bar = px.bar(h_agg, x="hour_bucket_label", y=["actual", "predicted"], barmode="group", title="Average Crimes by Hour Bucket")

    return mae_str, fig_line, fig_bar

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
