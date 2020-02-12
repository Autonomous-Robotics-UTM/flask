import base64
import io

from flask import Flask, render_template, request, Response
import pandas as pd
import os
import time
import csv
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

#csv stuff (starting live graph csv)
df = []
csv_name = 'csv/' + str(int(time.time())) + '.csv'
with open(csv_name, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Steer Command"])

#grab all csv files in directory
file_names = os.listdir('./csv/')
file_names = [file for file in file_names if '.csv' in file]
for file in file_names: df.append(int(file[:-4]))
df.sort(reverse=True)

#globals
start = 0
last = 0
imgs = 0

#server setup
exst = ['https://fonts.googleapis.com/css?family=Roboto']
app = Flask(__name__)
dash_app = dash.Dash('__name__', server=app, routes_pathname_prefix='/graph/', external_stylesheets=exst)

#html layout for graph part of website
dash_app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Button('Clear', id='clear-button'),
                html.Button('Pause', id='pause-button', n_clicks=0),
                dcc.Upload(html.Button('Upload File'), id='upload-button')
            ], style={'justify-content': 'center', 'align-items': 'center', 'display': 'flex', 'width': '49%'}),
            html.Div([
                html.Label('Images Collected: '),
                html.Label('0', id='img-counter')
            ], style={'justify-content': 'center', 'align-items': 'center', 'display': 'flex', 'width': '49%'}),
            html.Div([
                html.Label('I want to see the last: '),
                dcc.Input(
                    value=0,
                    type="number",
                    min=0,
                    id='last-num'
                )
            ], style={'justify-content': 'center', 'align-items': 'center', 'display': 'flex', 'width': '49%'})
        ], style={'display': 'inline-block', 'width': '49%'}),
        dcc.Dropdown(
            id='past-dropdown',
            options=[{'label': time.ctime(df[i]), 'value': i} for i in range(len(file_names))],
            value=0,
            style={'display': 'inline-block', 'width': '49%'}
        )
    ]),
    html.Div([
        dcc.Graph(id='live-graph', style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(id='graph', style={'display': 'inline-block', 'width': '49%'})
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    )
])

#dash callbacks
@dash_app.callback(
    [Output(component_id='img-counter', component_property='children'),
    Output(component_id='live-graph', component_property='figure')],
    [Input(component_id='interval-component', component_property='n_intervals'),
     Input(component_id='last-num', component_property='value'),
     Input(component_id='upload-button', component_property='contents')],
    [State('upload-button', 'filename')]
)
def update_live_graph(n, value, contents, filename):
    global start, imgs, last
    data = []

    if value:
        last = value
    else:
        last = 0

    live = pd.read_csv(csv_name)
    short_live = live[start:][-last:]
    data.append({'type': 'line', 'x': short_live['Time'], 'y': short_live['Steer Command'], 'name': 'live'})

    if contents is not None:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))[start:len(live)][-last:]
                data.append({'type': 'line', 'x': df['Time'], 'y': df['Steer Command'], 'name': filename})

        except Exception as e:
            print(e)

    fig = {
        'data': data,
        'layout': {'title': {'text': 'Steer Commands over Time'},
                   'yaxis': [-1, 1]}
    }
    return imgs, fig

@dash_app.callback(
    Output(component_id='interval-component', component_property='n_intervals'),
    [Input(component_id='clear-button', component_property='n_clicks')]
)
def reset_graph(n):
    global start
    start = len(pd.read_csv(csv_name))
    return n

@dash_app.callback(
    [Output(component_id='pause-button', component_property='children'),
    Output(component_id='interval-component', component_property='interval')],
    [Input(component_id='pause-button', component_property='n_clicks')]
)
def pause_graph(n):
    if n%2 == 0:
        return 'Pause', 1000
    return 'Start', 60*60*1000

@dash_app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='past-dropdown', component_property='value')]
)
def past_graph_update(value):
    data = pd.read_csv('csv/' + str(df[value]) + '.csv')
    fig = {
        'data': [{'type': 'line',
                  'x': data['Time'],
                  'y': data['Steer Command']}],
        'layout': {'title': {'text': 'Steer Commands over Time'},
                   'yaxis': [-1, 1]}
    }
    return fig

#routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/graph/plot', methods=['POST'])
def plot_post():
    data = request.get_json()
    time, command = data['time'], data['command']
    with open(csv_name, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([time, command])
    return Response('Data Read!', headers={'status': 200})\

@app.route('/graph/imgs', methods=['POST'])
def imgs_post():
    global imgs
    data = request.get_json()
    num = data['imgs']
    imgs = num
    return Response('Data Read!', headers={'status': 200})

@app.route('/cmd', methods=['POST'])
def cmd_post():
    data = request.get_json()
    cmd = data['cmd']
    os.system(cmd)
    return Response('Data Read!', headers={'status': 200})

#main
if __name__ == "__main__":
    dash_app.run_server(host='0.0.0.0', port=8080)
