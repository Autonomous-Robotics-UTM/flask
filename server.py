from flask import Flask, render_template, request, Response
import pandas as pd
import time
import csv
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
        ),
    html.Button('Clear', id='button')
])

csv_name = str(int(time.time())) + '.csv'
with open(csv_name, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Steer Command"])
max_t = 5

def get_figure(data):
    fig = {
        'data': [{'type': 'line',
                  'x': data['Time'],
                  'y': data['Steer Command']}],
        'layout': {'title': {'text': 'Steer Commands over Time'},
                   'yaxis': [-1, 1]}
    }
    return fig

#dash callbacks
@dash_app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='interval-component', component_property='n_intervals')]
)
def update_output_div(n):
    return get_figure(pd.read_csv(csv_name))

@dash_app.callback(
    Output(component_id='interval-component', component_property='n_intervals'),
    [Input(component_id='button', component_property='n_clicks')]
)
def update_output_div(n):
    with open(csv_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Steer Command"])
    return 0

#routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/graph', methods=['POST'])
def graph_post():
    data = request.get_json()
    time, command = data['time'], data['command']
    with open(csv_name, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([time, command])
    return Response('Data Read!', headers={'status': 200})

if __name__ == "__main__":
    dash_app.run_server(host='0.0.0.0', port=8080)
