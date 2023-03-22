#!/usr/bin/env python3

import dash
from dash import html
from dash.dependencies import Input, Output
import subprocess
from dash import dcc
import pandas as pd
from pathlib import Path
import datetime as dt
import plotly.express as px
import numpy as np

# Define the Dash app
app = dash.Dash(__name__)
app.title = "Tesla Dashboard"

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1("Tesla Inc"),
    html.Div(id="live-update-text"),
    html.H2("Tesla Price Over Time", style={"text-align": "center"}),
    dcc.Graph(id="live-update-graph"),
    html.Br(),
    html.H2("Volume On 5 days", style={"text-align": "center"}),
    dcc.Graph(id="live-update-volume"),
    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0),
    html.Br(),
    html.H2("Tesla Volatility Over Time", style={"text-align": "center"}),
    dcc.Graph(id="live-update-volatility"),
    html.H1("Daily Report"),
    html.Ul(id='live-update-report'),
    html.Footer(
            html.I([
                'Website : ',
                html.A("YahooFinance", href="https://fr.finance.yahoo.com/quote/TSLA?p=TSLA"),
                '. Code ',
                html.A("GitHub", href="https://github.com/MarineBqt/ProjetLinux"),
                '.',
            ])
        ),
])
#style={'backgroundColor': '#2b2a2a','margin': '-5','padding': '0','boxSizing': 'border-box','color': '#dcdcdc'}

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


#Update the graph 1 (line chart)
def update_graph(n):
    df = pd.read_csv('history.csv', skiprows=[0],names=['timestamp', 'price'])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    fig=px.line(df, x="timestamp", y="price",markers=True)
    fig.update_yaxes(tickprefix="$")
    fig.update_xaxes(
        title_text="time",
        rangeslider_visible=False,
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[19.9, 14.5], pattern="hour"),  # hide hours outside of 20pm-14.30pm
        ],
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor="gray",
        )
    )
    fig.update_layout(template="plotly_dark")
    return fig


# Define a function to update the graph on the dashboard
@app.callback(
    dash.dependencies.Output("live-update-volume", "figure"),
    dash.dependencies.Input("interval-component", "n_intervals")
)


#Update the graph 2 (bar chart)
def update_graph2(n):
    df = pd.read_csv('report.csv', skiprows=[0],names=['timestamp','prev_close', 'open_price','cap_boursiere','volume','target'])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df=df.tail(5)
    fig=px.bar(df,x='timestamp',y="volume",color="volume",color_continuous_scale='RdBu', text='volume')
    fig.update_xaxes(title_text="date")
    fig.update_layout(template="plotly_dark")
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

#Update the graph 3 volatility (line chart)
@app.callback(
    dash.dependencies.Output("live-update-volatility", "figure"),
    dash.dependencies.Input("interval-component", "n_intervals")
)

def update_graph3(n):
    df = pd.read_csv('history.csv', skiprows=[0], names=['timestamp', 'price'])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    # Calculate the daily returns and volatility
    df["returns"] = df["price"].pct_change()
    df["volatility"] = df["returns"].rolling(window=30).std() * np.sqrt(30) #volatility over 30 days

    # Plot the volatility over time
    fig = px.line(df, x="timestamp", y="volatility", markers=True)
    fig.update_yaxes(title_text="volatility")
    fig.update_xaxes(
        title_text="time",
        rangeslider_visible=False,
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[19.9, 14.5], pattern="hour"),  # hide hours outside of 20pm-14.30pm
        ],
    )
    fig.update_traces(line=dict(color='orange'))
    fig.update_layout(template="plotly_dark")
    return fig

#Executer l'app dash
if __name__ == '__main__':
   app.run_server(host='0.0.0.0', port=8050, debug=True)
