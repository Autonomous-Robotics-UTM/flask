from flask import Flask, render_template, request, Response
import plotly
import plotly.graph_objs as go
import pandas as pd
import time
import csv
import numpy as np
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = Flask(__name__)

dash_app = dash.Dash('__name__', server=app, routes_pathname_prefix='/graph/')
dash_app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )
])

csv_name = str(int(time.time())) + '.csv'
with open(csv_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Steer Command"])
max_t = 5

@dash_app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='interval-component', component_property='n_intervals')]
)
def update_output_div(n):
    data = pd.read_csv(csv_name)
    fig = {
        "data": [{"type": "line",
                  "x": data['Time'],
                  "y": data['Steer Command']}],
        "layout": {"title": {"text": "Steer Commands over Time"}}
    }
    return fig

#routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/graph', methods=['POST'])
def graph_post():
    data = request.get_json()
    time, command = data['time'], data['command']
    with open(csv_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time, command])
    return Response('Data Read!', headers={'status': 200})

if __name__ == "__main__":
    dash_app.run_server(debug=True)
