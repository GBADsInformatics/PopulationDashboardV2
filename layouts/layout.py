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

GBADSLOGOB = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-Black-sm.png"

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


title = html.Div(
                [
                    html.Img(src=GBADSLOGOB, className="header-logo"),
                    html.H1('Livestock Population')
                ]
                )

tabs = html.Div([
    
    html.H1(" "),
    html.H2(" "),
        dbc.Tabs(
            [
                dbc.Tab(label="Graph", active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label="Map",active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label='Download Data', active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label='Metadata', active_label_style=ACTIVE_TAB_STYLE)
            ],
        id='tabs', style={"padding": "1rem 1rem", "position":"fixed"})
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
