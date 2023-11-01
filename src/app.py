# import dash
# from dash import dcc, html
# import plotly.graph_objs as go
# import random
# import pandas as pd

# ################### back end #################
# app = dash.Dash(__name__)

# def update_graph(n_intervals):
#     data = {
#         'Time': range(n_intervals),
#         'Value': [random.random() for _ in range(n_intervals)]
#     }
#     df = pd.DataFrame(data)
#     trace = go.Scatter(
#         x=df['Time'],
#         y=df['Value'],
#         mode='lines+markers',
#         line=dict(color='magenta')  # Setting the line color to cyan
#     )
#     return {'data': [trace]}

# ################## front end ##################
# app.layout = html.Div([
#     html.Div(  # Adding a bar on top
#         [
#             html.H1(
#                 "Pred Maintenance System",
#                 style={
#                     'textAlign': 'center',
#                     'color': 'cyan',
#                 }
#             )
#         ],
#         style={
#             'backgroundColor': '#00214f',
#             'padding': '20px',
#         }
#     ),
#     dcc.Graph(id='live-update-graph'),
#     dcc.Interval(
#         id='interval-component',
#         interval=1*1000,  # in milliseconds
#         n_intervals=0
#     )
# ],
# style={'backgroundColor': '#2f2f2f'}  # Setting the background color to dark gray
# )

# @app.callback(
#     dash.dependencies.Output('live-update-graph', 'figure'),
#     [dash.dependencies.Input('interval-component', 'n_intervals')]
# )
# def update_output(n_intervals):
#     return update_graph(n_intervals)

# ################## front end ##################

# if __name__ == '__main__':
#     app.run_server(debug=True)



###################

# import dash
# from dash import dcc, html
# import plotly.graph_objs as go
# import random
# import pandas as pd
# import math

# ################### back end #################
# app = dash.Dash(__name__)
#Initiate the app 
server = app.server

# def update_graph_1(n_intervals):
#     data = {
#         'Time': range(n_intervals),
#         'Value': [random.random() for _ in range(n_intervals)]
#     }
#     df = pd.DataFrame(data)
#     trace = go.Scatter(
#         x=df['Time'],
#         y=df['Value'],
#         mode='lines+markers',
#         line=dict(color='cyan')
#     )
#     return {'data': [trace]}

# def update_graph_2(n_intervals):
#     data = {
#         'Time': range(n_intervals),
#         'Value': [0.75*random.random() for _ in range(n_intervals)]
#     }
#     df = pd.DataFrame(data)
#     trace = go.Scatter(
#         x=df['Time'],
#         y=df['Value'],
#         mode='lines+markers',
#         line=dict(color='magenta')
#     )
#     return {'data': [trace]}

# ################## front end ##################
# app.layout = html.Div([
#     html.Div(  # Adding a bar on top
#         [
#             html.H1(
#                 "Pred Maintenance System",
#                 style={
#                     'textAlign': 'center',
#                     'color': 'cyan',
#                 }
#             )
#         ],
#         style={
#             'backgroundColor': '#00214f',
#             'padding': '20px',
#         }
#     ),
#     html.Div(  # Container for the graphs
#         [
#             html.Div(  # Left graph
#                 [
#                     dcc.Graph(id='live-update-graph-1'),
#                 ],
#                 style={'width': '50%', 'display': 'inline-block'}
#             ),
#             html.Div(  # Right graph
#                 [
#                     dcc.Graph(id='live-update-graph-2'),
#                 ],
#                 style={'width': '50%', 'display': 'inline-block'}
#             )
#         ],
#         style={'display': 'flex'}
#     ),
#     dcc.Interval(
#         id='interval-component',
#         interval=1*1000,  # in milliseconds
#         n_intervals=0
#     )
# ])

# @app.callback(
#     [dash.dependencies.Output('live-update-graph-1', 'figure'),
#      dash.dependencies.Output('live-update-graph-2', 'figure')],
#     [dash.dependencies.Input('interval-component', 'n_intervals')]
# )
# def update_output(n_intervals):
#     figure_1 = update_graph_1(n_intervals)
#     figure_2 = update_graph_2(n_intervals)
#     return figure_1, figure_2

# ################## front end ##################

# if __name__ == '__main__':
#     app.run_server(debug=True)


##################################

import dash
from dash import dcc, html
import plotly.graph_objs as go
import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np  # Importing the numpy library

################### back end #################
app = dash.Dash(__name__)


def generate_data(n_intervals):
    now = datetime.now()
    times = [(now - timedelta(seconds=i)).strftime('%Y-%m-%d %H:%M:%S') for i in reversed(range(n_intervals))]
    values = [random.random() for _ in range(n_intervals)]
    return times, values

def update_graph(times, values, graph_id):
    if graph_id == 2:
        values = np.log(np.array(values) + 1)  # Applying log to the values for the second graph
    trace = go.Scatter(
        x=times,
        y=values,
        mode='lines+markers',
        line=dict(color='cyan' if graph_id == 1 else 'magenta')
    )
    layout = go.Layout(
        xaxis=dict(title='Time'),
        title='Temperature' if graph_id == 1 else 'Torque'  # Setting the title based on graph_id
    )
    return {'data': [trace], 'layout': layout}

################## front end ##################
app.layout = html.Div([
    html.Div(  # Adding a bar on top
        [
            html.H1(
                "Pred Maintenance System",
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
                    dcc.Graph(id='live-update-graph-1'),
                ],
                style={'width': '50%', 'display': 'inline-block'}
            ),
            html.Div(  # Right graph
                [
                    dcc.Graph(id='live-update-graph-2'),
                ],
                style={'width': '50%', 'display': 'inline-block'}
            )
        ],
        style={'display': 'flex'}
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    [dash.dependencies.Output('live-update-graph-1', 'figure'),
     dash.dependencies.Output('live-update-graph-2', 'figure')],
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_output(n_intervals):
    times_1, values_1 = generate_data(n_intervals)  # Generate data for the first graph
    times_2, values_2 = generate_data(n_intervals)  # Generate data for the second graph
    figure_1 = update_graph(times_1, values_1, graph_id=1)
    figure_2 = update_graph(times_2, values_2, graph_id=2)
    return figure_1, figure_2

################## front end ##################

if __name__ == '__main__':
    app.run_server(debug=True)
