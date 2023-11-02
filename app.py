import dash
from dash import dcc, html
import plotly.graph_objs as go
import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np  # Importing the numpy library

################### back end #################
app = dash.Dash(__name__, external_stylesheets=[
    {
        'selector': '.dark-theme .Select-control, .dark-theme .Select-multi-value-wrapper, .dark-theme .Select-clear-zone, .dark-theme .Select-arrow-zone',
        'rule': 'background-color: black;'
    }
])

#Initiate the app 
server = app.server

def generate_data(n_intervals, graph_id):
    now = datetime.now()
    times = [(now - timedelta(seconds=i)).strftime('%Y-%m-%d %H:%M:%S') for i in reversed(range(n_intervals))]
    
    if graph_id == 1:  # Temperature graph
        values = [random.uniform(280, 299) for _ in range(n_intervals)]
    elif graph_id == 2:  # Torque graph
        values = [random.uniform(30, 50) for _ in range(n_intervals)]
    else:  # Rotation graph
        values = [random.uniform(1300, 1500) for _ in range(n_intervals)]
    
    return times, values


def update_graph(times, values, graph_id):
    # if graph_id == 2:
    #     values = np.log(np.array(values) + 1)
    trace = go.Scatter(
        x=times,
        y=values,
        mode='lines+markers',
        line=dict(color='cyan' if graph_id == 1 else 'magenta' if graph_id == 2 else 'orange')
    )
    layout = go.Layout(
        xaxis=dict(
            title='Time',
            gridcolor='grey',
            titlefont=dict(
                color='cyan'
            ),
            tickfont=dict(
                color='cyan'
            )
        ),
        yaxis=dict(
            gridcolor='grey',
            titlefont=dict(
                color='cyan'
            ),
            tickfont=dict(
                color='cyan'
            )
        ),
        title='Temperature' if graph_id == 1 else 'Torque' if graph_id == 2 else 'Rotation',
        titlefont=dict(
            color='cyan'
        ),
        paper_bgcolor='#111111',
        plot_bgcolor='#111111'
    )
    return {'data': [trace], 'layout': layout}


################## front end ##################
app.layout = html.Div([
    html.Div(  # Adding a bar on top
        [
            html.H1(
                "Predective Maintenance Technology Demonstrator System",
                style={
                    'textAlign': 'center',
                    'color': 'cyan',
                }
            )
        ],
        style={
            'backgroundColor': '#00214f',
            'padding': '20px',
        }
    ),
    
    html.Div(  # Container for the graphs
        [
            html.Div(  # Left graph
                [
                    dcc.Graph(id='live-update-graph-3'),
                ],
                style={'width': '33%', 'display': 'inline-block', 'backgroundColor': '#111111'}
            ),
            html.Div(  # middle graph
                [
                    dcc.Graph(id='live-update-graph-1'),
                ],
                style={'width': '33%', 'display': 'inline-block', 'backgroundColor': '#111111'}
            ),
            html.Div(  # left graph
                [
                    dcc.Graph(id='live-update-graph-2'),
                ],
                style={'width': '33%', 'display': 'inline-block', 'backgroundColor': '#111111'}
            )
        ],
        style={'display': 'flex', 'backgroundColor': '#111111'}
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
], style={'backgroundColor': '#111111', 'color': 'white'})


@app.callback(
    [dash.dependencies.Output('live-update-graph-1', 'figure'),
     dash.dependencies.Output('live-update-graph-2', 'figure'),
     dash.dependencies.Output('live-update-graph-3', 'figure')],  # Adding output for third graph
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)

# def update_output(n_intervals):
#     times, values = generate_data(n_intervals)
#     figure_1 = update_graph(times, values, graph_id=1)
#     figure_2 = update_graph(times, values, graph_id=2)
#     figure_3 = update_graph(times, values, graph_id=3)  # Adding update for third graph
#     return figure_1, figure_2, figure_3

def update_output(n_intervals):
    times_1, values_1 = generate_data(n_intervals, graph_id=1)  # Temperature
    times_2, values_2 = generate_data(n_intervals, graph_id=2)  # Torque
    times_3, values_3 = generate_data(n_intervals, graph_id=3)  # Rotation
    figure_1 = update_graph(times_1, values_1, graph_id=1)
    figure_2 = update_graph(times_2, values_2, graph_id=2)
    figure_3 = update_graph(times_3, values_3, graph_id=3)
    return figure_1, figure_2, figure_3


################## front end ##################

if __name__ == '__main__':
    app.run_server(debug=True)
