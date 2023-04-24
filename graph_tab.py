import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc

plot_config = {'displayModeBar': True,
          'displaylogo': False}

graph = dcc.Graph(id = 'graph1', config = plot_config)

tab1_content = graph