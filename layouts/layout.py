import dash
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
from dash import dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from app import app

load_figure_template('LUX')

GBADSLOGOB = "./assets/GBADsLogo.png"

ACTIVE_TAB_STYLE = {
    "color": "#FFA500"
}

CONTENT_STYLE = {
    "top":"8rem",
    "margin-left": "25rem",
    "margin-right": "8rem",
    "bottom": "2rem",
    "padding": "7rem 2rem 2rem",
    "overflow": "scroll"
}

CONTENT_STYLE_GRAPHS = {
    "top":"8rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "5rem 2rem 2rem",
    "position": "fixed"
}

CONTENT_STYLE_TABLES = {
    "top":"8rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "5rem 2rem 2rem",
    "overflow": "scroll",
    "position": "fixed"
}

plot_config = {'displayModeBar': True,
          'displaylogo': False}

###-------------Components------------------------------------

sidebar_metadata = html.Div(
        [
        dbc.Row(
            [
                html.H4('Options', className="sidebar"),
            ],
            style={"height": "5vh"}
            ),
        dbc.Row(
            [  
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset',value ='faostat', persistence=True, persistence_type='session'),
                html.H6(" ")
            ], className="sidebar"
        ),
    ]
)

sidebar_download = html.Div(
    [
        dbc.Row(
            [
                html.H4('Options', className="sidebar"),
            ],
            style={"height": "5vh"}
            ),
        dbc.Row(
            [
                html.H6("Select multiple:", id='choice-title'),
                dcc.RadioItems(
                ['Species', 'Countries'], 'Species', inline=True, id='choice', persistence_type='session', persistence=True
                ),
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value='faostat', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Country:"),
                dcc.Dropdown(id = 'country', value = 'Ethiopia', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species', value = ['Cattle'], persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Start year:"),
                dcc.Dropdown(id = 'start year', value = 1996, persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("End year:"),
                dcc.Dropdown(id = 'end year', value = 2020, persistence_type='session', persistence=True)
                ], className="sidebar"
            )
    ]
)

sidebar = html.Div(
    [
        dbc.Row(
            [
                html.H4('Options', className="sidebar"),
            ],
            style={"height": "5vh"}
            ),
        dbc.Row(
            [
                    html.H6("Select multiple:", id='choice-title'),
                    dcc.RadioItems(
                    ['Species', 'Countries'], 'Species', inline=True, id='choice', persistence_type='session',persistence=True
                    ),
                    html.H6(" "),
                    html.H6("Dataset:"),
                    dcc.Dropdown(id = 'dataset', value='faostat', persistence_type='session', persistence=True),
                    html.H6(" "),
                    html.H6("Country:"),
                    dcc.Dropdown(id = 'country', value = 'Ethiopia', persistence_type='session', persistence=True),
                    html.H6(" "),
                    html.H6("Species:"),
                    dcc.Dropdown(id = 'species', value = ['Cattle'],persistence_type='session', persistence=True),
                    html.H6(" "),
                    html.H6("Start year:"),
                    dcc.Dropdown(id = 'start year', value = 1996, persistence_type='session', persistence=True),
                    html.H6(" "),
                    html.H6("End year:"),
                    dcc.Dropdown(id = 'end year', value = 2020, persistence_type='session', persistence=True),
                    html.H6(" "),
                    html.H6("Graph type:"),
                    dcc.Dropdown(id = 'plot', value = 'stacked bar', options = ['stacked bar','scatter line'], persistence_type='session', persistence=True),
                ], className="sidebar"
            )
    ]
)

sidebar_map = html.Div(
    [
        dbc.Row(
            [
                html.H4('Options', className="sidebar"),
            ],
            style={"height": "5vh"}
            ),
        dbc.Row(
            [
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value = 'faostat', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species-map', value = 'Cattle', multi=False,persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Year:"),
                dcc.Dropdown(id = 'year-map', value = 1990,persistence_type='session', persistence=True),
                ], className="sidebar"
            )
    ]
)

title = html.Div(
                [
                    html.Img(src=GBADSLOGOB, className="header-logo"),
                    html.H1('Livestock Population')
                ]
                )

tabs = html.Div([
    
        dbc.Tabs(
            [
                dbc.Tab(label="Graph", activeTabClassName = "nav-link-active", tabClassName="nav-link"),
                dbc.Tab(label="Map", activeTabClassName="nav-link-active", tabClassName="nav-link"),
                dbc.Tab(label='Download Data', activeTabClassName="nav-link-active", tabClassName="nav-link"),
                dbc.Tab(label='Metadata', activeTabClassName="nav-link-active", tabClassName="nav-link")
            ],
        id='tabs')
]
)

###--------------Build the layout------------------------------------

app_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(title, width=6),
                dbc.Col(tabs, width='auto')
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(id='tabs-content'))
            ]
            ),
    ],
    fluid=True
    )
