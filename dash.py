import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Load data
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str}
)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1('Airline Performance Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    html.Div(["Input Year: ",
              dcc.Input(id='input-year', value='2010', type='number',
                        style={'height': '50px', 'font-size': 35})
              ],
             style={'font-size': 40}),

    html.Br(),

    html.Div([
        dcc.Graph(id='line-plot'),
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='buble-chart'),
        dcc.Graph(id='sunburst-chart')
    ])
])

# Callback for multiple graphs
@app.callback(
    [Output('line-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('sunburst-chart', 'figure'),
     Output('buble-chart', 'figure')],
    [Input('input-year', 'value')]
)
def update_graphs(entered_year):
    # Filter data by year
    df = airline_data[airline_data['Year'] == int(entered_year)]

    # Line plot: Month vs Average Flight Delay
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    line_fig = go.Figure(data=go.Scatter(x=line_data['Month'],
                                         y=line_data['ArrDelay'],
                                         mode='lines+markers',
                                         marker=dict(color='green')))
    line_fig.update_layout(title='Month vs Average Flight Delay Time',
                           xaxis_title='Month',
                           yaxis_title='Arrival Delay (minutes)')

    # Pie chart: Distance group proportion
    pie_fig = px.pie(df, values='Flights', names='DistanceGroup',
                     title='Distance Group Proportion by Month')

    # Bar chart: Flights by Destination State
    bar_data = df.groupby(['DestState'])['Flights'].sum().reset_index()
    bar_fig = px.bar(bar_data, x="DestState", y="Flights",
                     title='Total Flights by Destination State')

    # Sunburst chart: Reporting airline and flights
    sun_fig = px.sunburst(df, path=['Month', 'DestStateName'], values='Flights',
                          title='Flight Distribution Hierarchy')

    # Bubble chart: Reporting airline vs number of flights
    bub_data = df.groupby('Reporting_Airline')['Flights'].sum().reset_index()
    bub_fig = px.scatter(bub_data, x="Reporting_Airline", y="Flights", size="Flights",
                         hover_name="Reporting_Airline", title='Reporting Airline vs Number of Flights', size_max=60)

    return line_fig, pie_fig, bar_fig, sun_fig, bub_fig


# Run the app only when this script is executed directly
if __name__ == '__main__':
    app.run()
