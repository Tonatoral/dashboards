
import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

def color_scale(value):
    if value < 50:
        return "#FF0000"#red
    elif value >= 50 and value <= 80:
        return "#FFFF00" #yellow
    elif value > 80:
        return "#00FF00" #green


# In[10]:


# Load your data
df = pd.read_csv('DataModelCoverage.csv')
df['color'] = df['Coverage'].apply(color_scale)

dfmap = pd.read_csv('DataModelCoverageforMap.csv')
dfmap['color'] = dfmap['Coverage'].apply(color_scale)

# Create the sunburst plot
sunburst = px.sunburst(df, color='color', values='Coverage', path=['Region','Country','Brand','Model','Coverage'],hover_name='Country')

# Create the choropleth map
map = px.choropleth(dfmap, locations='Country',color= 'Coverage',labels={'Coverage':'Coverage in %'},color_continuous_scale=[[0, "red"], [0.60, "yellow"],[0.8, "green"], [1, "green"]], range_color=(0,100), title='Coverage in Europe',hover_data=['Country'],scope='europe')

# Create the Dash app
app = dash.Dash()
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='sunburst', children=[
        dcc.Tab(label='Coverage', value='sunburst', children=[
            dcc.Graph(figure=sunburst)
        ]),
        dcc.Tab(label='Planner view', value='map', children=[
            dcc.Graph(figure=map)
        ])
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




