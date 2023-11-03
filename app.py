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
    elif graph_id == 3:  # Rotation graph
        values = [random.uniform(1300, 1500) for _ in range(n_intervals)]
    else:  # Speed graph
        values = [random.uniform(50, 70) for _ in range(n_intervals)]
    
    return times, values


def update_graph(times, values, graph_id):
    # if graph_id == 2:
    #     values = np.log(np.array(values) + 1)
    trace = go.Scatter(
        x=times,
        y=values,
        mode='lines+markers',
        # line=dict(color='cyan' if graph_id == 1 else 'magenta' if graph_id == 2 else 'orange')
        line=dict(color='cyan')
    )
    layout = go.Layout(
        height=300,
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
        title='Temperature' if graph_id == 1 else 'Torque' if graph_id == 2 else 'Rotation' if graph_id == 3 else 'Speed',
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
                "Predictive Maintenance Technology Demonstrator Dashboard",
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
    
     html.Div(  # Container for the graphs and gif
        [
            html.Div(  # Container for left graphs
                [
                    html.Div(  # hopper
                        [
                            dcc.Graph(id='live-update-graph-4'),
                        ],
                        style={'width': '100%', 'display': 'inline-block', 'backgroundColor': '#111111'}
                    ),
                    html.Div(  # rotation graph
                        [
                            dcc.Graph(id='live-update-graph-3'),
                        ],
                        style={'width': '100%', 'display': 'inline-block', 'backgroundColor': '#111111'}
                    )
                ],
                style={'width': '33%', 'display': 'inline-block', 'backgroundColor': '#111111'}
            ),
            html.Div(  # Container for gif
                [
                    html.Img(src='/assets/dashboardscada3.gif', height='300px', width='450px')
                ],
                style={'width': '35%', 'display': 'inline-block', 'backgroundColor': '#111111', 'margin-top': '160px'}
            ),
            html.Div(  # Container for right graph (Rotation)
                [
                    html.Div(  # Temperature graph
                        [
                            dcc.Graph(id='live-update-graph-1'),
                        ],
                        style={'width': '100%', 'display': 'inline-block', 'backgroundColor': '#111111'}
                    ),
                    html.Div(  # Temperature graph
                        [
                            dcc.Graph(id='live-update-graph-2'),
                        ],
                        style={'width': '100%', 'display': 'inline-block', 'backgroundColor': '#111111'}
                    )
                    # dcc.Graph(id='live-update-graph-3'),
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
     dash.dependencies.Output('live-update-graph-3', 'figure'),
     dash.dependencies.Output('live-update-graph-4', 'figure')],  # Adding output for fourth graph
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
    times_4, values_4 = generate_data(n_intervals, graph_id=4)  # Speed
    
    figure_1 = update_graph(times_1, values_1, graph_id=1)
    figure_2 = update_graph(times_2, values_2, graph_id=2)
    figure_3 = update_graph(times_3, values_3, graph_id=3)
    figure_4 = update_graph(times_4, values_4, graph_id=4)
    return figure_1, figure_2, figure_3, figure_4


################## front end ##################

if __name__ == '__main__':
    app.run_server(debug=True)
