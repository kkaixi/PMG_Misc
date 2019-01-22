# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 16:57:13 2018
test dash
@author: tangk
Plot things interactively using Dash

"""
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import h5py

def get_test(tc,channel):
    # this function is only for retrieving tests stored in P:/Data Analysis/Data
    # only reads one tc and one channel at a time. 
    # returns time and data from one channel and one tc
    tc = '/' + tc.replace('-','N')
    channel = 'X' + channel
      
#    with pd.HDFStore('P:\\Data Analysis\\Test\\Tests.h5', mode='r+') as test:
    with h5py.File('P:\\Data Analysis\\Data\\' + tc[1:3] + '\\Tests.h5','r') as test:
        if channel in test[tc].dtype.names:
            t = test[tc]['XT_10000_0']
            x = test[tc][channel]
        else:
            t = None
            x = None 
    
    return t, x

def get_test_info():
    directory = 'P:\\Data Analysis\\Data\\'
    test_names = pd.read_csv(directory + 'test_names.csv',header=None)
    channel_names = pd.read_csv(directory + 'channel_names.csv',header=None)
    return np.concatenate(test_names.values), np.concatenate(channel_names.values)


tests, channels = get_test_info()
tests.sort()
channels.sort()
#%%


app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Graph(
        id='time_series',
        figure={
            'data': [
                {'x': [], 'y': []}],
            'layout': {
                'title': ' ',
                'titlefont':{'size':20},
            'showlegend': True
            }
        },
        style={'height': '750'}
    ),
    
    html.Div([
    html.Div(dcc.Dropdown(id = 'tc_entry',
                 options = [{'label': i, 'value': i} for i in tests],
                 value=' '),
            style = {'width': '48%', 'display': 'inline-block'}),
                 
    html.Div(dcc.Dropdown(id = 'ch_entry',
                 options = [{'label': i, 'value': i} for i in channels],
                 value=' '),
            style = {'width': '48%', 'display': 'inline-block', 'float': 'right'})]),
    html.Div([
    html.Div(dcc.Dropdown(id = 'tc_entry_2',
                 options = [{'label': i, 'value': i} for i in tests],
                 value=' '),
            style = {'width': '48%', 'display': 'inline-block'}),
                 
    html.Div(dcc.Dropdown(id = 'ch_entry_2',
                 options = [{'label': i, 'value': i} for i in channels],
                 value=' '),
            style = {'width': '48%', 'display': 'inline-block', 'float': 'right'})])
#    dcc.Input(id='tc_entry', value=' ', type='text')
])



@app.callback(
        dash.dependencies.Output(component_id='time_series',component_property='figure'),
        [dash.dependencies.Input(component_id='tc_entry',component_property='value'),
         dash.dependencies.Input(component_id='ch_entry',component_property='value'),
         dash.dependencies.Input(component_id='tc_entry_2',component_property='value'),
         dash.dependencies.Input(component_id='ch_entry_2',component_property='value')])
def update_figure(tc,ch,tc2,ch2):
    #initialize the new graph
    new_graph = {'data'  : [],
                 'layout': {'title'     : ' ',
                            'titlefont' : {'size': 20},
                            'showlegend': True}}
    
    #if no search in either fields, plot nothing
    if (tc in [' ', None] or ch in [' ', None]) and (tc2 in [' ', None] or ch2 in [' ', None]):
        new_graph['data'].append({'x': [], 'y': []})
        return new_graph
    
    # if first fields are not empty, then add to plot
    if not(tc in [' ', None]) and not(ch in [' ', None]):
        t, x = get_test(tc, ch)
        if (x[1:]==0).all():
            t = [0]
            x = [x[0]]
            new_graph['data'].append({'x': t, 'y': x, 'name': tc + ',' + ch, 'mode': 'markers','line': {'color': '#182952'}})
        else:
            new_graph['data'].append({'x': t, 'y': x, 'name': tc + ',' + ch,'line': {'color': '#182952'}})
    
    # if second fields are not empty, then add to plot
    if not(tc2 in [' ', None]) and not(ch2 in [' ', None]):
        t2, x2 = get_test(tc2,ch2)
        if (x2[1:]==0).all():
            t2 = [0]
            x2 = [x2[0]]
            new_graph['data'].append({'x': t2, 'y': x2, 'name': tc2 + ',' + ch2, 'mode': 'markers','line': {'color': '#ff5da2'}})
        else:
            new_graph['data'].append({'x': t2, 'y': x2, 'name': tc2 + ',' + ch2,'line': {'color': '#ff5da2'}})

    return new_graph

if __name__=='__main__':
    app.run_server()