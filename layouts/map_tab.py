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
# from layouts import styling 
import json

# def create_map(df, species, year):

#     world_map_file_path = "../data/world_map_110m.geojson"

#     with open(world_map_file_path) as file:
#         world_map_json = json.load(file)

#     iso_code_file_path = "../data/FAOSTAT_mappings.csv"
#     iso_code_df = pd.read_csv(iso_code_file_path)
#     merged_df = pd.merge(df, iso_code_df, how='inner', left_on='country', right_on='Short name', left_index=False, right_index=False)

#     print(merged_df)
#     max_val = merged_df[merged_df.population].max()
#     print(max_val)

#     fig = px.choropleth_mapbox(merged_df, 
#         geojson=world_map_json,
#         color='population',
#         range_color=(0,max_val),
#         hover_data=['country', 'population'],
#         featureidkey='properties.ISO_A3_EH',
#         color_continuous_scale='magma_r',
#         center={'lat':19, 'lon':11},
#         mapbox_style='carto-positron',
#         opacity=0.5,
#         zoom=1
#     )
#     # fig.update_geos(fitbounds='locations')
#     fig.update_layout(
#         margin=dict(t=0, l=0, r=0, b=0),
#     )

#     return(fig)

map = dcc.Graph(id = 'map')

content = dbc.Row(children=
            [
            styling.sidebar_map,
            dbc.Col(map)
            ]
        )

# faostat = pd.read_csv('../data/faostat.csv')
# map = create_map(faostat, 'Cattle', '1997')
