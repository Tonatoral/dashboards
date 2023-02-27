import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# Load data
df = pd.read_csv('DataModelDetailedwDataTypes.csv')

# Define function to create color scale
def color_scale(value):
    if value < 50:
        return "#FF0000"#red
    elif value >= 50 and value <= 80:
        return "#FFFF00" #yellow
    elif value > 80:
        return "#00FF00" #green

# Add color column to dataframe
df['color'] = df['Coverage'].apply(color_scale)
df['gap'] = 100 - df['Coverage']

# Define sunburst charts
fig_coverage = px.sunburst(df, color='color', path=['Region','Country','Brand','Model','Volume','Coverage'],
                           hover_name='Model',
                           maxdepth=2,
                           title='Click in the chart to explore our data coverage',
                           branchvalues='total',
                           values='Volume',
                           custom_data=['Region','Country','Brand','Model'])
fig_coverage.update_traces(textinfo='label+percent entry')

fig_gap = px.sunburst(df, color='color', path=['Region','Country','Brand','Model','gap'],
                       hover_name='Model',
                       maxdepth=3,
                       title='Click in the chart to explore the GAPS in our data coverage',
                       branchvalues='remainder',
                       values='gap',
                      custom_data=['Region','Country','Brand','Model']
                      )
fig_gap.update_traces(textinfo='label')

# Define tables
table_coverage = dcc.Graph(id='table-coverage')
table_gap = dcc.Graph(id='table-gap')

# Define slider
slider_years = dcc.RangeSlider(
    id='slider-years',
    min=df['Year'].min(),
    max=df['Year'].max(),
    value=[df['Year'].min(), df['Year'].max()],
    marks={str(year): str(year) for year in df['Year'].unique()},
    step=None
)

#Define Tab conents
#tab1_content= dbc.


# Define external style
#external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__,external_stylesheets=external_stylesheets) #Open the app and loads external style

#Define local style
app= dash.Dash(__name__) # Open the app and loads css file in /assets folder locally

#Define app layout
app.layout = dbc.Container([
    dcc.Store(id="store"),
    html.H1("Coverage Dashboard"),
    html.Hr(),
    dbc.Tabs([
        dbc.Tab([
            dbc.Row([dbc.Col([
                dcc.Dropdown(
                    id="megatrends",
                    placeholder='Select a megatrend',
                    options=[
                        {"label": "ADAS", "value": "ADAS"},
                        {"label": "EV", "value": "EV"},
                        {"label": "other Megatrends", "value": "other"}
                    ], style={'width': '50%'}
                )
            ], width={'size': 5, 'offset': 0}),
                dbc.Col([slider_years],width={'size': 5, 'offset': 0},align='right')
            ]),#End of first row
            dbc.Row([
                dbc.Col([dcc.Graph(id='sunburst-coverage', figure=fig_coverage,
                                    config = {'staticPlot': False,  # not a statig plot
                                    'scrollZoom': True,
                                    'doubleClick': 'reset',  # resets on double click
                                    'showTips': True,  # shows tips to help new users
                                    'displayModeBar': True,  # displays toolbar on top of graph
                                    'watermark': True
                                    }
                                    )]),
                dbc.Col([table_coverage])
            ])
        ],label='Coverage view',tab_id="coverage"), #End of coverage tab
        dbc.Tab([
            dbc.Row([dbc.Col([
                dcc.Dropdown(
                    id="megatrends",
                    placeholder='Select a megatrend',
                    options=[
                        {"label": "ADAS", "value": "ADAS"},
                        {"label": "EV", "value": "EV"},
                        {"label": "other Megatrends", "value": "other"}
                    ], style={'width': '50%'}
                )
            ], width={'size': 5, 'offset': 0}),
                dbc.Col([slider_years],width={'size': 5, 'offset': 0},align='right')
            ]),#End of first row
            dbc.Row([
                dbc.Col([dcc.Graph(id='sunburst-gap', figure=fig_gap,
                                    config = {'staticPlot': False,  # not a statig plot
                                    'scrollZoom': True,
                                    'doubleClick': 'reset',  # resets on double click
                                    'showTips': True,  # shows tips to help new users
                                    'displayModeBar': True,  # displays toolbar on top of graph
                                    'watermark': True
                                    }
                                    )]),
                dbc.Col([table_gap])
            ]) # End of second row
        ],label="Planner view", tab_id="planner"), #End of Planner Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Input(placeholder='Enter a VIN or list of VINs (, separated)', type='text', value=''),
                    # End of input
                    dbc.Button("Search", color="primary", className="mt-3", size="sm", n_clicks=0)
                ], width={'size': 3})  # End of column
            ])  # End of Row
        ],label="Carparc view",tab_id="carparc")           #End of carparc Tab
    ],              #Close Squarebracekt of Tabs
    id="tabs",
    active_tab="coverage"
    ) # End of Tabs
], fluid=True)  # End of Container






# app.layout = html.Div([
#     dcc.Tabs([
#         dcc.Tab(label='Coverage View', children=[
#             html.Div([
#                 html.H1("Coverage Dashboard Mock-up", style={'text-align': 'center'}), # Adds title to the tab
#                 #Adds input field to enter a VIN Number
#                 dcc.Input(
#                     placeholder='Enter a VIN or list of VINs (, separated)',
#                     type='text',
#                     value='',
#                     style={'width': '50%'}
#                 ),
#
#                 #Adds Dropdown menu to select megatrends
#                 dcc.Dropdown(id="megatrends",
#                              placeholder='Select a megatrend',
#                              options=[
#                                  {"label":"ADAS","value":"ADAS"},
#                                  {"label":"EV","value":"EV"},
#                                  {"label":"other Megatrends","value":"other"}
#                              ],
#                              style={'width': '50%'}),
#
#                 html.Div([
#                     dcc.Graph(id='sunburst-coverage', figure=fig_coverage,
#                                     config = {'staticPlot': False,  # not a statig plot
#                                     'scrollZoom': True,
#                                     'doubleClick': 'reset',  # resets on double click
#                                     'showTips': True,  # shows tips to help new users
#                                     'displayModeBar': True,  # displays toolbar on top of graph
#                                     'watermark': True
#                                     }
#                                     )], className='six columns'
#                          ),
#                 html.Div([table_coverage], className='six columns'),
#             ], className='row'),
#         ]),
#         dcc.Tab(label='Planner View', children=[
#             html.H1("Planner View Mock-up", style={'text-align': 'center'}),
#             html.Div([
#                 html.Div([dcc.Graph(id='sunburst-gap', figure=fig_gap)], className='six columns'),
#                 html.Div([table_gap], className='six columns'),
#             ], className='row'),
#         ]),
#     ]),
#     html.Div(slider_years),
# ])

# Define callback for coverage table
@app.callback(
    Output('table-coverage', 'figure'),
    #Output('table-gap','figure'),
    [Input('sunburst-coverage', 'clickData'),
     Input('slider-years', 'value')])
def update_table_coverage(click_data, year_range):
    if click_data is None:
        df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    else:
        region = click_data['points'][0]['customdata'][0]
        country = click_data['points'][0]['customdata'][1]
        brand = click_data['points'][0]['customdata'][2]
        model = click_data['points'][0]['customdata'][3]
        df_temp=df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
        if region =="(?)":
            df_filtered=df_temp
        elif country == "(?)":
            df_filtered = df_temp[(df_temp['Region'] == region)]
        elif brand == "(?)":
            df_filtered = df_temp[(df_temp['Region'] == region) & (df_temp['Country'] == country)]
        elif model == "(?)":
            df_filtered = df_temp[(df_temp['Region'] == region) & (df_temp['Country'] == country) & (df_temp['Brand'] == brand)]
        else:
            df_filtered = df_temp[(df_temp['Region'] == region) & (df_temp['Country'] == country) & (df_temp['Brand'] == brand)&(df_temp['Model'] == model)]

    fig = go.Figure(data=[go.Table(header=dict(values=['Region','Country','Brand','Model','Year','Coverage'],
                                               fill_color='paleturquoise',
                                               align='left'),
                                   cells=dict(values=[df_filtered.Region,df_filtered.Country,df_filtered.Brand,df_filtered.Model,df_filtered.Year,df_filtered.Coverage],
                                              fill_color='lavender',
                                              align='left'))
                          ])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
