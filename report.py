import plotly.offline as pyo
import plotly.express as px
import pandas as pd

df = pd.read_csv('DataModelCoverage.csv')
df['color']=df['Coverage'].apply(color_scale)
fig=px.sunburst(df, color='color', values='Coverage', path=['Region','Country','Brand','Model','Coverage'],hover_name='Country')

dfmap = pd.read_csv('DataModelCoverageforMap.csv')
dfmap['color']=dfmap['Coverage'].apply(color_scale)
fig1=px.choropleth(dfmap, locations='Country',color= 'Coverage',labels={'Coverage':'Coverage in %'},color_continuous_scale=[[0, "red"], [0.60, "yellow"],[0.8, "green"], [1, "green"]], range_color=(0,100), title='Coverage in Europe',hover_data=['Country'],scope='europe')

tabs_settings = {
    'type': 'tabs',
    'tabs': [{'label': 'Coverage', 'value': 'tab-1'},
             {'label': 'Planner View', 'value': 'tab-2'}]
}

tab_1 = pyo.plot(fig, auto_open=False, output_type='div')
tab_2 = pyo.plot(fig1, auto_open=False, output_type='div')

fig_tabs = {
    'data': [],
    'layout': {
        'title': 'Report Tabs',
        'template': 'plotly_dark',
        'updatemenus': [tabs_settings],
        'xaxis': {
            'showgrid': False,
            'zeroline': False,
            'showticklabels': False,
        },
        'yaxis': {
            'showgrid': False,
            'zeroline': False,
            'showticklabels': False,
        },
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font': {
            'color': 'white'
        },
    },
    'frames': [{
            'name': 'tab-1',
            'value': tab_1
        },
        {
            'name': 'tab-2',
            'value': tab_2
        }
    ]
}

pyo.plot(fig_tabs, auto_open=True, filename='Report.html')
