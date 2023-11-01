import dash
from dash import dcc, html
import plotly.graph_objs as go
import random
import pandas as pd

################### back end #################
app = dash.Dash(__name__)

def update_graph(n_intervals):
    data = {
        'Time': range(n_intervals),
        'Value': [random.random() for _ in range(n_intervals)]
    }
    df = pd.DataFrame(data)
    trace = go.Scatter(
        x=df['Time'],
        y=df['Value'],
        mode='lines+markers'
    )
    return {'data': [trace]}

################## front end ##################
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    dash.dependencies.Output('live-update-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_output(n_intervals):
    return update_graph(n_intervals)

################## front end ##################

if __name__ == '__main__':
    app.run_server(debug=True)
