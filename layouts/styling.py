import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from dash import dash_table

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

CONTENT_STYLE = {
    "top":"8rem",
    "margin-left": "25rem",
    "margin-right": "8rem",
    "bottom": "2rem",
    "padding": "7rem 2rem 2rem",
    "overflow": "scroll"
}

MAP_STYLE = {
    "top":"8rem",
    "margin-left": "24rem",
    "margin-right": "8rem",
    "bottom": "2rem",
    "padding": "7rem 2rem 2rem",
    "overflow": "scroll"
}

plot_config = {'displayModeBar': True,
          'displaylogo': False}

sidebar_download = html.Div(
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
                dcc.Dropdown(id = 'dataset', value='faostat'),
                html.H6(" "),
                html.H6("Country:"),
                dcc.Dropdown(id = 'country', value='Spain'),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species', value = ['Asses', 'Cattle']),
                html.H6(" "),
                html.H6("Start year:"),
                dcc.Dropdown(id = 'start year', value = 1990),
                html.H6(" "),
                html.H6("End year:"),
                dcc.Dropdown(id = 'end year', value = 2001)
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

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
                dcc.Dropdown(id = 'dataset', value='faostat'),
                html.H6(" "),
                html.H6("Country:"),
                dcc.Dropdown(id = 'country', value='Spain'),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species', value = ['Asses', 'Cattle']),
                html.H6(" "),
                html.H6("Start year:"),
                dcc.Dropdown(id = 'start year', value = 1990),
                html.H6(" "),
                html.H6("End year:"),
                dcc.Dropdown(id = 'end year', value = 2001),
                html.H6(" "),
                html.H6("Graph type:"),
                dcc.Dropdown(id = 'plot', value = 'stacked bar', options = ['stacked bar','scatter line']),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

sidebar_map = html.Div(
    [
        html.H4("Options"),
        html.Hr(),
        dbc.Nav(
            [  
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value='faostat'),
                html.H6(" "),
                html.H6("Country:"),
                dcc.Dropdown(id = 'country-map', value = 'Canada', multi=True),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species-map', value = 'Cattle', multi=False),
                html.H6(" "),
                html.H6("Year:"),
                dcc.Dropdown(id = 'year-map', value = 1990),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)