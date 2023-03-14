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

# Lire le fichier CSV et charger les données dans un DataFrame
df = pd.read_csv('history.csv',skiprows=[0],names=['timestamp', 'price'])

# Convertir les timestamps en objets datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')


# Créer l'application Dash
app = dash.Dash(__name__)
app.title = "Tesla viewership"


#Mise en page du dashboard
app.layout = html.Div([
    html.H1('Tesla Inc',style={'text-align': 'center'}),
    html.Div(id='live-update-text'),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # Mettre à jour toutes les 10 seconde
        n_intervals=0
    ),
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                go.Scatter(
                    x=df['timestamp'],
                    y=df['price'],
                    mode='lines'
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date',
		       'rangeslider': {'visible': True}
		},
                yaxis={'title': 'Stock Prices'},
		title='Evolution du prix de l\'action TESLA',
        	template='seaborn', #'plotly_dark'
            )
        },
    ),
])

# Définir la fonction de mise à jour des données
@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])

def update_metrics(n):
    # Lire à nouveau le fichier CSV pour récupérer les dernières données
    df = pd.read_csv('history.csv', names=['timestamp', 'price'])
    last_price = df['price'].iloc[-1]
    return f'Dernière valeur du prix : {last_price}'


#Executer l'app dash
if __name__ == '__main__':
   app.run_server(host='0.0.0.0', port=8050, debug=True)

