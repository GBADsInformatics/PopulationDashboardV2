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

def create_map(df, species, year, dataset):

    world_map_file_path = "data/world_map_110m.geojson"

    with open(world_map_file_path) as file:
        world_map_json = json.load(file)

    iso_code_file_path = "data/FAOSTAT_mappings.csv"
    iso_code_df = pd.read_csv(iso_code_file_path)
    merged_df = pd.merge(df, iso_code_df, how='inner', left_on='country', right_on='Short name', left_index=False, right_index=False)

    # Filter by species 
    merged_df = merged_df.loc[merged_df['year'] == year]
    merged_df = merged_df.loc[merged_df['species'] == species]
    max_val = merged_df['population'].max()
    min_val = merged_df['population'].min()

    title = 'Population of %s in %s by Country <br><sup>Datasource: %s</sup>' % (species, year, dataset)

    fig = px.choropleth_mapbox(merged_df, 
        geojson=world_map_json,
        locations='ISO3',
        color='population',
        range_color=(min_val,max_val),
        hover_data=['country', 'population'],
        featureidkey='properties.ISO_A3_EH',
        color_continuous_scale='magma_r',
        center={'lat':19, 'lon':11},
        mapbox_style='carto-positron',
        opacity=0.5,
        zoom=1
    )

    fig.update_layout(
        title_text = title
    )
    fig.update_geos(fitbounds="locations", visible=True)

    return(fig)

map = dcc.Graph(id = 'map', config = styling.plot_config)

content = dbc.Row(children=
            [
            styling.sidebar_map,
            dbc.Col(map)
            ]
        )