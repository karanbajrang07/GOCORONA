import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.graph_objects as go
from scrap import *
import os
# import urllib
import re
import pandas as pd
import urllib.request
import datetime
global str

global df
df=update_data()
df=pd.read_csv("data_covid1.csv")
app = dash.Dash()



labels = df["Name"]
values = df["Total Confirmed cases(Indian)"]
options=['Total Confirmed cases(Indian)','Total Confirmed cases(Foreign)', 'Cured', 'Death']
drop_down = []
for i in options:
    drop_down.append({'label':str(i),'value':i})


app.layout = html.Div([
    html.Div(id='last-update', style={'display':'none'}),
    dcc.Dropdown(id='count_case',options=drop_down,value='Total Confirmed cases(Indian)'),
    dcc.Graph(
        id='graph'
    ),
    html.Div([html.Button('Refresh Data', id='refresh-data')]),
    
])

@app.callback(Output('graph', 'figure'),
              [Input('count_case', 'value')])
def figure_update(selected_value):
    df[df[selected_value]>0][selected_value]
    return go.Figure(go.Pie(labels=df[df[selected_value]>0]["Name"], values=df[df[selected_value]>0][selected_value],textinfo='label',textposition='inside'))

@app.callback(
    Output('last-update','children'),
    [Input('refresh-data','n_clicks')])
def refresh_data(value):
    
    global df
    
    df=update_data()
    df=pd.read_csv("data_covid1.csv")
    connection.close()
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    app.run_server()