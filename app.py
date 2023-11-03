##################################

import dash
from dash import dcc, html
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objs as go
import random
import pytz
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

data = {
    'Predicted Failure Date': ['27/02/2024', '03/03/2024', '17/03/2024', '29/04/2024', '13/05/2024', '23/06/2024', '09/09/2024', '11/09/2024'],
    'Prediction': ['Failure 1 - turbulent flow rate', 'Failure 2 - bearing wear', 'Failure 3 - resin leakage', 'Failure 1 - turbulent flow rate', 'Failure 4 - abnormal temp', 'Failure 1 - turbulent flow rate', 'Failure 2 - bearing wear', 'Failure 5 - unknown'],
    'RUL': ['61%', '57%', '51%', '45%', '39%', '21%', '13%', '1%']
}
df = pd.DataFrame(data)


########### RUL graph data
# Convert the initial RUL value to a decimal
initial_rul = 0.77  # corresponding to 77%
# current_date = datetime.datetime.now().strftime('%d/%m/%Y')
# current_date = datetime.now().strftime('%d/%m/%Y')

# Define your time zone
my_timezone = pytz.timezone('Asia/Singapore')  # Replace 'Asia/Singapore' with your actual time zone

# Get the current date and time in your time zone
current_date = datetime.now(my_timezone).strftime('%d/%m/%Y')

# Parse the dates to datetime objects
date_previous = datetime.strptime('02/11/2023', '%d/%m/%Y')
date_current = datetime.strptime(current_date, '%d/%m/%Y')

# Calculate the number of days between the two dates
days_between = (date_current - date_previous).days

# Calculate the time elapsed
date_initial = datetime.strptime('01/03/2023', '%d/%m/%Y')
time_elapsed_days = (datetime.now() - date_initial).days

# Calculate the total degradation
total_degradation = days_between * 6.3e-4

# Calculate degNow
deg_now_decimal = initial_rul - total_degradation

# Convert degNow back to a percentage format
deg_now_percentage = f'{deg_now_decimal * 100:.2f}%'

# Replace 'degNow' in your data
dataRUL = {
    'Date': ['01/03/2023', '02/11/2023', current_date, '27/02/2024', '03/03/2024', '17/03/2024', '29/04/2024', '13/05/2024', '23/06/2024', '09/09/2024', '11/09/2024'],
    'RUL': ['95%', '77%', deg_now_percentage, '61%', '57%', '51%', '45%', '39%', '21%', '13%', '1%']
}

dfRUL = pd.DataFrame(dataRUL)

# Convert 'RUL' to numeric for plotting
dfRUL['RUL_numeric'] = dfRUL['RUL'].str.rstrip('%').astype(float)

# Create the figure
fig = go.Figure()

# Add the line plot
fig.add_trace(go.Scatter(x=dfRUL['Date'], y=dfRUL['RUL_numeric'], mode='lines+markers', name='RUL over Time'))

# Highlight the current point
highlight_x = [current_date]
highlight_y = [deg_now_decimal * 100]  # converting to percentage format
fig.add_trace(go.Scatter(x=highlight_x, y=highlight_y, mode='markers', marker=dict(color='magenta', size=15), name='Current Date'))


# Define the background color shapes
shapes = [
    dict(type='rect', xref='paper', yref='y', x0=0, y0=0, x1=1, y1=20, fillcolor='red', opacity=0.5, line_width=0),
    dict(type='rect', xref='paper', yref='y', x0=0, y0=20, x1=1, y1=60, fillcolor='yellow', opacity=0.5, line_width=0),
    dict(type='rect', xref='paper', yref='y', x0=0, y0=60, x1=1, y1=100, fillcolor='green', opacity=0.5, line_width=0)
]

# Define annotations for risk levels
annotations = [
    dict(x=1.05, y=10, xref='paper', yref='y', text='High Risk', showarrow=False, font=dict(color='red', size=15)),
    dict(x=1.05, y=40, xref='paper', yref='y', text='Medium Risk', showarrow=False, font=dict(color='orange', size=15)),
    dict(x=1.05, y=80, xref='paper', yref='y', text='Low Risk', showarrow=False, font=dict(color='green', size=15))
]

# Update the layout to include the shapes and format the x-axis dates
fig.update_layout(
    shapes=shapes,
    annotations=annotations,
    yaxis=dict(range=[0, 100], title='RUL (%)'),
    xaxis=dict(
        tickangle=-45,
        nticks=20,
        tickfont=dict(size=10),
        tickformat="%d/%m/%Y"
    ),
    title='Remaining Useful Life over Time',
    paper_bgcolor='#111111',
    plot_bgcolor='#111111',
    font=dict(color='white'),
)
# fig.update_layout(
#     shapes=shapes,
#     yaxis=dict(range=[0, 100], title='RUL (%)'),
#     title='RUL over Time',
#     paper_bgcolor='#111111',
#     plot_bgcolor='#111111',
#     font=dict(color='white'),
# )

#############

# Calculate the time remaining
date_next_failure = datetime.strptime('27/02/2024', '%d/%m/%Y')
#time_remaining_days = (date_next_failure - datetime.now()).days
time_remaining_days = (date_next_failure - date_current).days

# Create the donut chart
fig_donut = go.Figure(data=[go.Pie(labels=df['Prediction'], values=df['RUL'].str.rstrip('%').astype(int), hole=.3)])

fig_donut.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=0, b=0),
    legend=dict(
        font=dict(
            color="white"
        )
    )
)

# Create the table
table = html.Table(
    # Header
    [html.Tr([html.Th(col, style={'border': '1px solid white'}) for col in df.columns])] +
    # Body
    [html.Tr([html.Td(df.iloc[i][col], style={'border': '1px solid white'}) for col in df.columns]) for i in range(len(df))],
    style={'margin-top': '20px', 'border-collapse': 'collapse'}
)

def generate_data(n_intervals, graph_id):
    #now = datetime.now()
    my_timezone = pytz.timezone('Asia/Singapore')
    now = datetime.now(my_timezone)
    
    # times = [(now - timedelta(seconds=i)).strftime('%Y-%m-%d %H:%M:%S') for i in reversed(range(n_intervals))]
    # Generate a list of time strings in one-second intervals
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
        title='Flow Temperature (°C)' if graph_id == 1 else 'Clamp Torque (N-m)' if graph_id == 2 else 'Motor Rotation (rpm)' if graph_id == 3 else 'Hopper Speed (rpm)',
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
    html.Div(  # Adding an overview box
        [
            html.H2(
                " Overview ",
                style={
                'textAlign': 'center',
                'color': 'magenta',
                'font-family': 'Arial, sans-serif',  # This line changes the font
                'font-size': '24px',  # This line changes the font size
                'font-weight': 'bold'  # This line makes the font bold
                }
            ),
            html.P(
                "Real Time Sensor data streaming via Synthetic Data Generation.",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                    'padding': '10px',
                    'backgroundColor': '#00214f',
                    'border': '2px solid cyan',
                    'borderRadius': '10px',
                    'margin': '20px'
                }
            )
        ]
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
                style={'width': '33%', 'display': 'inline-block', 'backgroundColor': '#111111', 'margin-top': '160px'}
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
    ),
    html.Div([  # Container for the squares
        html.Div([  # Individual square
            html.H4(
        "Machine Type",
        style={
            'font-family': 'Arial, sans-serif',
            'color': 'cyan'
        }),
            html.P("Injection Moulding Machine #6")
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
        }),
        html.Div([  # Individual square
            html.H4(
        "Health Status",
        style={
            'font-family': 'Arial, sans-serif',
            'color': 'cyan'
        }),
            html.P(deg_now_percentage)
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
        }),
        html.Div([  # Individual square
            html.H4(
        "Predicted Downtime",
        style={
            'font-family': 'Arial, sans-serif',
            'color': 'cyan'
        }),
            html.P("11/9/2024")
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
        }),
        html.Div([  # Individual square
            html.H4(
        "Degradation Rate",
        style={
            'font-family': 'Arial, sans-serif',
            'color': 'cyan'
        }),
            html.P("-6.3e-4")
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
        }),
    ], style={
        'textAlign': 'center'
    }),
    html.Div(  # Adding a Root-Cause Analysis box
        [
            html.H2(
                " Root-Cause Analysis ",
                style={
                    'textAlign': 'center',
                    'color': 'magenta',
                    'font-family': 'Arial, sans-serif',  # This line changes the font
                    'font-size': '24px',  # This line changes the font size
                    'font-weight': 'bold'  # This line makes the font bold
                }
            ),
            html.P(
                "Future Failure Class Prediction.",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                    'padding': '10px',
                    'backgroundColor': '#00214f',
                    'border': '2px solid cyan',
                    'borderRadius': '10px',
                    'margin': '20px'
                }
            ),
            
            html.Div([
            # Donut chart
            dcc.Graph(figure=fig_donut),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
            # Table
            table,
            ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '50px'}
            ),
            
        ]
    ),
    html.Div(  # Adding a machine lifetime box
    [
        html.H2(
            " Machine Lifetime ",
            style={
                'textAlign': 'center',
                'color': 'magenta',
                'font-family': 'Arial, sans-serif',  # This line changes the font
                'font-size': '24px',  # This line changes the font size
                'font-weight': 'bold'  # This line makes the font bold
            }
        ),
        html.P(
            "Remaining Useful Life projection from predicted failure cases.",
            style={
                'textAlign': 'center',
                'color': 'white',
                'padding': '10px',
                'backgroundColor': '#00214f',
                'border': '2px solid cyan',
                'borderRadius': '10px',
                'margin': '20px'
            }
        )
    ]
),
    html.Div([
        dcc.Graph(figure=fig)
    ], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': '#111111'}
),

 html.Div([  # Container for the info squares
        html.Div([  # Individual square
            html.H4(
                "Current Status",
                style={
                    'font-family': 'Arial, sans-serif',
                    'color': 'cyan'
                }),
            html.P("OK")
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
        }),
        html.Div([  # Individual square for Time Elapsed
            html.H4(
                "Time Elapsed",
                style={
                    'font-family': 'Arial, sans-serif',
                    'color': 'cyan'
                }),
            html.P(f'{time_elapsed_days} days')
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
        }),
        html.Div([  # Individual square
            html.H4(
                "Current Time",
                style={
                    'font-family': 'Arial, sans-serif',
                    'color': 'cyan'
                }),
            html.P(current_date)
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
            # ... rest of the style attributes ...
        }),
        html.Div([  # Individual square
            html.H4(
                "Current RUL",
                style={
                    'font-family': 'Arial, sans-serif',
                    'color': 'cyan'
                }),
            html.P(deg_now_percentage)
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
            # ... rest of the style attributes ...
        }),
        html.Div([  # Individual square
            html.H4(
                "Next Failure Pred",
                style={
                    'font-family': 'Arial, sans-serif',
                    'color': 'cyan'
                }),
            html.P('Turbulent Flow Rate')
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
            # ... rest of the style attributes ...
        }),
        html.Div([  # Individual square
            html.H4(
                "Time Remaining",
                style={
                    'font-family': 'Arial, sans-serif',
                    'color': 'cyan'
                }),
            html.P(f'{time_remaining_days} days')
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
            # ... rest of the style attributes ...
        }),
        html.Div([  # Individual square
            html.H4(
                "Predicted Downtime",
                style={
                    'font-family': 'Arial, sans-serif',
                    'color': 'cyan'
                }),
            html.P('27/02/2024')
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
            # ... rest of the style attributes ...
        }),
        html.Div([  # Individual square
            html.H4(
                "Predicted RUL",
                style={
                    'font-family': 'Arial, sans-serif',
                    'color': 'cyan'
                }),
            html.P('61%')
        ], style={
            'width': '18%',
            'backgroundColor': '#00214f',
            'border': '2px solid cyan',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'inline-block'
            # ... rest of the style attributes ...
        }),
    ], style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'space-around'
    }),   
    
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
