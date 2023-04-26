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

# def create_map(df, geojson, species):
#     fig = px.choropleth_mapbox(
# Subclass ChoroplethMap
# class ChoroplethMap(PlotlyGraph):

#     # Constructor
#     # Params:
#     # geojson_file = geojson file
#     # data_locations (str) = column header of the dataframe that contains unique area names to be mapped (the names will be mapped to featureidkey's names)
#     # color_data_by (str) = column header that contains categorical values to be colored
#     # featureidkey (str) = has the format of 'properties.<col_name>', col_name is the column header of the geojson file that contains unique area names
#     # hover_data (list) = a list of column headers of dataframe whose data will be displayed on choropleth map
#     def __init__(self, graph_name, dataframe, data_source, geojson_file, data_locations, color_data_by, featureidkey, hover_data):
#         self.geojson_file = geojson_file
#         self.data_locations = data_locations
#         self.color_data_by = color_data_by
#         self.featureidkey = featureidkey
#         self.hover_data = hover_data
#         super().__init__(graph_name, dataframe, data_source)
    
#     def get_figure(self):
#         max_val = self.dataframe[self.color_data_by].max()
#         fig = px.choropleth_mapbox(self.dataframe, geojson=self.geojson_file, locations=self.data_locations,
#             color=self.color_data_by,
#             range_color=(0,max_val),
#             hover_data=self.hover_data,
#             featureidkey=self.featureidkey,
#             color_continuous_scale='magma_r',
#             center={'lat':19, 'lon':11},
#             mapbox_style='carto-positron',
#             opacity=0.5,
#             zoom=1
#         )
#         # fig.update_geos(fitbounds='locations')
#         fig.update_layout(
#             margin=dict(t=0, l=0, r=0, b=0),
#         )
#         return fig