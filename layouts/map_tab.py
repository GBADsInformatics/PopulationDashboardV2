import dash
import dash_bootstrap_components as dbc
from dash import html, dash_table
import pandas as pd
from dash import dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from layouts import layout
import json

# Potentially switch this to leaflet https://dash-leaflet.herokuapp.com/

my_color_scale = [[0.0, '#4c5c73'], [0.1, '#5D6C81'], [0.2, '#6F7C8F'], [0.3, '#818C9D'], [0.4, '#939DAB'],
                  [0.5, '#A5ADB9'], [0.6, '#B7BDC7'], [0.7, '#C9CED5'], [0.8, '#DBDEE3'], [0.9, '#EDEEF1'],
                  [1.0, '#FFFFFF']]

def create_map(merged_df, dataset, species, year):

    max_val = merged_df['population'].max()
    min_val = merged_df['population'].min()

    title = 'Population of %s in %s by Country <br><sup>Datasource: %s</sup>' % (species, year, dataset)

    fig = px.choropleth(merged_df, 
        locations='iso3',
        color='population',
        range_color=(0,max_val),
        hover_data=['country', 'population'],
        color_continuous_scale='sunset',
        center={'lat':19, 'lon':11},
    )

    fig.update_geos(
        visible=False, resolution=50,
        showcountries=True, countrycolor="Black"
    )

    fig.update_layout(
        title_text = title,
        legend=dict(orientation='h',
        yanchor="bottom")
    )

    return(fig)

map = dcc.Graph(id = 'map', config = layout.plot_config)

content = dbc.Row(
    [
        dbc.Col(layout.sidebar_map, 
                xs=dict(order=1, size=12),
                sm=dict(order=1, size=3)
                ),
        dbc.Col(map,
                xs=dict(order=2, size=12),
                sm=dict(order=2, size='auto'))
    ], className='root-container'
)