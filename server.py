from flask import Flask, render_template
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import dash_html_components as html
import dash

app = Flask(__name__)

dash_app = dash.Dash('__name__', server=app, routes_pathname_prefix='/graph/')
dash_app.layout = html.Div(id='bargraph')

#routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/graph')
def graph():
	bar = create_plot()
	return render_template('graph.html', plot=bar)


if __name__ == "__main__":
    dash_app.run_server(debug=True)
