import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
import graph_helpers as gh

load_figure_template('LUX')

GBADSLOGOB = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-Black-sm.png"

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "8rem",
    "left": 0,
    "bottom": "2rem",
    "width": "24rem",
    "padding": "2rem 2rem 2rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

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

###-------------Components------------------------------------
sidebar = html.Div(
    [
        html.H4("Options"),
        html.Hr(),
        dbc.Nav(
            [  
                html.H6("Select multiple:", id='choice-title'),
                dcc.RadioItems(
                ['Species', 'Countries'], 'Species', inline=True, id='choice'
                ),
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value='eurostat'),
                html.H6(" "),
                html.H6("Country:"),
                dcc.Dropdown(id = 'country', value='Spain'),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species', value = ['Bovines', 'Asses and Mules', 'Goats']),
                html.H6(" "),
                html.H6("Start year:"),
                dcc.Dropdown(id = 'start year', value = 1990),
                html.H6(" "),
                html.H6("End year:"),
                dcc.Dropdown(id = 'end year', value = 2001),
                html.H6(" "),
                html.H6("Graph type:"),
                dcc.Dropdown(id = 'plot', value = 'stacked bar', options = ['stacked bar','scatter','map']),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

title = html.Div([
                    html.Img(src=GBADSLOGOB, className="header-logo"),
                    html.H2('Livestock Population')
                ],
                style={"padding": "1rem 1rem", "position":"fixed"}
                )

tabs = html.Div([
    
    html.H1(" "),
        dbc.Tabs(
            [
                dbc.Tab(label="Graph", active_label_style=ACTIVE_TAB_STYLE),
                #dbc.Tab(label="Map",active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label='Download Data', active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label='Metadata', active_label_style=ACTIVE_TAB_STYLE)
            ],
        id='tabs')
]
)

content = html.Div(dcc.Loading(type='default'),
                   id="page-content", 
                   style=CONTENT_STYLE)
###--------------Build the layout------------------------------------

app_layout = html.Div(

    children = [
        dbc.Row(children = [
            dbc.Col(title),
            dbc.Col(tabs)
        ]
        ),
        dbc.Row(
            [
            sidebar,
            dbc.Col(content)
            ],
            id='body-content'
        )
    ]

)

