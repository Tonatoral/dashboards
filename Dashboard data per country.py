import plotly.express as px
import pandas as pd
import plotly.offline as pyo

def color_scale(value):
    if value < 50:
        return "#FF0000"#red
    elif value >= 50 and value <= 80:
        return "#FFFF00" #yellow
    elif value > 80:
        return "#00FF00" #green

df=pd.read_csv('DataModelDetailedwDataTypes.csv')

df['color']=df['Coverage'].apply(color_scale)
fig=px.sunburst(df, color='color',path=['Region','Country','Brand','Model','Volume','Coverage'],
                hover_name='Model',
                #hover_data={'Columnname':False}, # removes a column from the hover data
                maxdepth=3,title='Click in the chart to explore our data coverage', 
                #template='ggplot2',
                branchvalues='total', 
                values='Volume'
               )
fig.update_traces(textinfo='label+ percent entry')

#pyo.plot(fig, auto_open=True, output_type='file', filename='sunburst.html')


df['gap']=100-df['Coverage']
print(df[['Coverage', 'gap']].head())
fig2=px.sunburst(df, color='color',path=['Region','Country','Brand','Model','gap'],
                hover_name='Model',
                #hover_data={'Columnname':False}, # removes a column from the hover data
                maxdepth=3,title='Click in the chart to explore the GAPS in our data coverage', 
                #template='ggplot2',
                branchvalues='remainder', #branchvalues='total',
                values='gap'
               )
fig2.update_traces(textinfo='label')

#pyo.plot(fig2, auto_open=True, output_type='file', filename='GAP_sunburst.html')

#dfmap = pd.read_csv('DataModelCoverageforMap.csv')
#dfmap['color']=dfmap['Coverage'].apply(color_scale)
#color_scale=[[0, "red"], [0.60, "yellow"],[0.8, "green"]]
#dfmap['Coverage_in_percentage'] = dfmap['Coverage'].astype(str) + '%'
#px.choropleth(dfmap, locations='Country',color= 'color', title='Coverage in Europe',hover_data=['Coverage_in_percentage'],scope='europe')

