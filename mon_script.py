#!/usr/bin/env python3

import dash
from dash import html
from dash.dependencies import Input, Output
import subprocess
from dash import dcc
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import datetime as dt
import plotly.graph_objs as go


# Define the Dash app
app = dash.Dash(__name__)
app.title = "Tesla Dashboard"

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1("Tesla Inc"),
    html.Div(id="live-update-text"),
    dcc.Graph(id="live-update-graph"),
    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0),
    html.H1("Daily Report"),
    html.Ul(id='live-update-report')
])


# Define a function to update the text on the dashboard
@app.callback(
    dash.dependencies.Output("live-update-text", "children"),
    dash.dependencies.Input("interval-component", "n_intervals")
)

def update_metrics(n):
    # Lire à nouveau le fichier CSV pour récupérer les dernières données
    df = pd.read_csv('history.csv', names=['timestamp', 'price'])
    last_price = df['price'].iloc[-1]
    return f'Dernière valeur du prix : {last_price}'

# Define a function to update the graph on the dashboard
@app.callback(
    dash.dependencies.Output("live-update-graph", "figure"),
    dash.dependencies.Input("interval-component", "n_intervals")
)


#Update the graph
def update_graph(n):
    df = pd.read_csv('history.csv', skiprows=[0],names=['timestamp', 'price'])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["price"], name="Price"))
    fig.update_layout(title="Bitcoin Price Over Time", xaxis_title="Date", yaxis_title="Price (USD)")
    return fig

# Define a function to update the text on the dashboard
@app.callback(
    dash.dependencies.Output("live-update-report", "children"),
    dash.dependencies.Input("interval-component", "n_intervals")
)

def update_report(n):
    # Lire à nouveau le fichier CSV pour récupérer les dernières données
    df = pd.read_csv('report.csv', skiprows=[0],names=['prev_close', 'open_price','cap_boursiere','volume','target'])
    last_row = df.iloc[-1].tolist()
    items=[html.Li(f"Previous close: {last_row[0]}"),
             html.Li(f"Open price: {last_row[1]}"),
             html.Li(f"Market capitalization: {last_row[2]} B"),
             html.Li(f"Volume: {last_row[3]} M"),
             html.Li(f"Target: {last_row[4]}")]
    return items

#Executer l'app dash
if __name__ == '__main__':
   app.run_server(host='0.0.0.0', port=8050, debug=True)
