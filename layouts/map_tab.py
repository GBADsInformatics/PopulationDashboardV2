import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from dash import dash_table
from layouts import styling 
import json

def create_map(merged_df, dataset, species, year):

    max_val = merged_df['population'].max()
    min_val = merged_df['population'].min()

    title = 'Population of %s in %s by Country <br><sup>Datasource: %s</sup>' % (species, year, dataset)

    fig = px.choropleth(merged_df, 
        locations='ISO3',
        color='population',
        range_color=(min_val,max_val),
        hover_data=['country', 'population'],
        color_continuous_scale='magma_r',
        center={'lat':19, 'lon':11},
    )

    fig.update_layout(
        title_text = title
    )

    return(fig)

map = dcc.Graph(id = 'map', config = styling.plot_config)

content = dbc.Row(children=
            [
            styling.sidebar_map,
            dbc.Col(map, style=styling.MAP_STYLE)
            ]
        )
