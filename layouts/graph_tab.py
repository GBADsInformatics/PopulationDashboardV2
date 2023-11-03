import dash
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
from dash import dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from dash import dash_table
from layouts import layout

def create_bar_plot(df, country, species):

    if type(country) == str:
        color_by = 'species'
        title = 'Population of Livestock in %s' % country
    else: 
        color_by = 'country'
        title = 'Population of %s' % species

    fig = px.bar(df, x='year', y='population', color=color_by,
                 color_discrete_sequence=px.colors.qualitative.Plotly, title = title)

    fig.update_xaxes(
        
        ticklabelmode="period",
        dtick = 1)

    return(fig)

def create_scatter_plot(df, country, species): 

    if type(country) == str:
        color_by = 'species'
        title = 'Population of Livestock in %s' % country
    else: 
        color_by = 'country'
        title = 'Population of %s' % species

    fig = px.line(df, x='year', y='population', color=color_by,
                 color_discrete_sequence=px.colors.qualitative.Plotly, markers=True, title = title)

    fig.update_xaxes(
        
        ticklabelmode="period",
        dtick = 1)
    
    return(fig)

graph = dcc.Graph(id = 'graph1', config = layout.plot_config)

content = dbc.Row(
    [
        dbc.Col(layout.sidebar, 
                xs=dict(order=1, size=12),
                sm=dict(order=1, size=3)
                ),
        dbc.Col(graph,
                xs=dict(order=2, size=12),
                sm=dict(order=2, size='auto'))
    ], className='root-container'
)
