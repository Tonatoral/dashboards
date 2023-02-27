# Video:    [Introduction to Dash Bootstrap - Styling your App](https://youtu.be/vqVwpL4bGKY)
# Docs:     [Dash Bootstrap Components:](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/)
#           [Dash Bootstrap Themes:](https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/)
from dash import Dash, dcc, html, Input, Output         # pip install dash
import dash_bootstrap_components as dbc         # pip install dash_bootstrap_components
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Berlin_crimes.csv")
df = df.groupby('District')[['Street_robbery', 'Drugs']].median()

app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("Stock Market Dashboard",
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Symbols'].unique())],
                         ),
            dcc.Graph(id='line-fig', figure={})
        ],# width={'size':5, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['PFE','BNTX'],
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Symbols'].unique())],
                         ),
            dcc.Graph(id='line-fig2', figure={})
        ], #width={'size':5, 'offset':0, 'order':2},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], justify='start'),  # Horizontal:start,center,end,between,around

    dbc.Row([
        dbc.Col([
            html.P("Select Company Stock:",
                   style={"textDecoration": "underline"}),
            dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(df['Symbols'].unique())],
                          labelClassName="mr-3"),
            dcc.Graph(id='my-hist', figure={}),
        ], #width={'size':5, 'offset':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        html.P(
                            "We're better together. Help each other out!",
                            className="card-text")
                    ),
                    dbc.CardImg(
                        src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif",
                        bottom=True),
                ],
                style={"width": "24rem"},
            )
        ], #width={'size':5, 'offset':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        )
    ], align="center")  # Vertical: start, center, end

], fluid=True)


@app.callback(
    [Output('pie_chart1', 'figure'),
     Output('pie_chart2', 'figure')],
    [Input('a_dropdown', 'value'),
     Input('b_dropdown', 'value'),
     Input('c_dropdown', 'value')]
)
def update_graph(dpdn_a, dpdn_b, dpdn_c):
    dff = df[:200]
    if dpdn_a is None or dpdn_b is None or dpdn_c is None:
        pie_fig = px.pie(dff, names=dff.index, values='Street_robbery', title='Street Robbery Berlin')\
            .update_layout(showlegend=False, title_x=0.5).update_traces(textposition='inside',  textinfo='label+percent')
        pie_fig2 = px.pie(dff, names=dff.index, values='Drugs', title='Drugs Berlin')\
            .update_layout(showlegend=False, title_x=0.5).update_traces(textposition='inside', textinfo='label+percent')
        return pie_fig, pie_fig2
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)