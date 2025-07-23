# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site Here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min = 0,
                                                    max = 10000,
                                                    step = 1000,
                                                    marks={0: '0',
                                                            2500 : '2500',
                                                            5000 : '5000',
                                                            7500 : '7500',
                                                            10000: '10000'},
                                                    value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'
                                                    )),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        all_df = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(all_df, values='class', 
            names='Launch Site', 
            title='Landing Success Rates by Site')
        return fig
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        site_df2 = site_df.groupby(['class']).size().reset_index(name = 'out_size')
        fig = px.pie(site_df2, values= 'out_size', names = 'class', title='Landing Outcomes for site {}'.format(entered_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart (entered_site, payload):
    df = spacex_df
    payload_min = payload[0]
    payload_max = payload[1]
    filtered_df = df[df['Payload Mass (kg)'].between(payload_min, payload_max, inclusive='both')]
    if entered_site == 'ALL':
        fig = px.scatter(x = filtered_df['Payload Mass (kg)'], 
                            y = filtered_df['class'], 
                            color = filtered_df['Booster Version Category'],
                            labels={
                                "x": "Payload Mass (kg)",
                                "y": "Class",
                                "color": "Booster Version Category"
                            },
                            title = 'Correlation between Payload and Success for all Sites')
        return fig
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(x = site_df['Payload Mass (kg)'], 
                            y = site_df['class'], 
                            color = site_df['Booster Version Category'],
                            labels={
                                "x": "Payload Mass (kg)",
                                "y": "Class",
                                "color": "Booster Version Category"
                            },
                            title = 'Correlation between Payload and Success for site {}'.format(entered_site))
        return fig
# Run the app
if __name__ == '__main__':
    app.run()
