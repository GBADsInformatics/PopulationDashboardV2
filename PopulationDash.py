import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
import dash_table
import utils.api_helpers as ah

GBADSLOGOB = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-Black-sm.png"
load_figure_template('LUX')
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

plot_config = {'displayModeBar': True,
          'displaylogo': False}

###--------------Read in data-----------------------------------

eurostat = pd.read_csv('data/eurostat.csv')
faostat = pd.read_csv('data/faostat.csv')
faotier1 = pd.read_csv('data/faostat.csv')
woah = pd.read_csv('data/oie.csv')
unfccc = pd.read_csv('data/unfccc.csv')

###--------------Build plots------------------------------------

def get_df(choice): 

    if choice == 'eurostat': 
        return(eurostat)
    elif choice == 'faostat':
        return(faostat)
    elif choice == 'faotier1': 
        return(faotier1)
    elif choice == 'woah':
        return(woah)
    elif choice == 'unfccc':
        return(unfccc)

def prep_df(df, country, species, start, end): 

    # Determine types 
    if type(country) == str: 
        df = df[df['country'] == country]
    else: 
        df = df[df['country'].isin(country)]
    
    if type(species) == str: 
        df = df[df['species'] == species]
    else: 
        df = df[df['species'].isin(species)]

    df = df[df['year'].between(start,end)]

    return(df)


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

###-------------Build dropdowns------------------------------------

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "8rem",
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

sidebar = html.Div(
    [
        html.H4("Options"),
        html.Hr(),
        dbc.Nav(
            [  
                html.H6("Compare by:"),
                dcc.RadioItems(
                ['Species', 'Country'], 'Species', inline=True, id='choice'
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
                dcc.Dropdown(id = 'plot', value = 'stacked bar', options = ['stacked bar','scatter']),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

title = html.Div(
            dbc.Row(
            dbc.Col(children = [
                html.Img(src=GBADSLOGOB, className="header-logo"),
                html.H2('Livestock Population')   
            ]
            )
            ),  
            style={"padding": "1rem 1rem"},
        )

graph = dbc.Col(
            dcc.Graph(id = 'graph1',config = plot_config),
            width = 8,
            style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px'}
            )


###--------------Build the layout------------------------------------

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div(children = [
                title,
                dbc.Row(
                    [
                    dbc.Col(sidebar),
                    graph
                    ]
                )
    ]
)


###--------------Call backs------------------------------------

# Initialize dataset dropdown
@app.callback(
    dash.dependencies.Output('dataset','options'),
    dash.dependencies.Input('choice','value')
)
def dataset_drop(name):
    
    dataset_options = ['eurostat','faostat','faotier1','woah','unfccc']

    return(dataset_options)

# Initialize all dropdowns and options
@app.callback(
    dash.dependencies.Output('country', 'options'),
    dash.dependencies.Output('country','multi'),
    dash.dependencies.Output('species','options'),
    dash.dependencies.Output('species','multi'),
    [dash.dependencies.Input('choice', 'value'),
     dash.dependencies.Input('dataset','value')]
)
def update_country_dropdown(name, data):

    # Update the ability to select multiple based on choice radio item
    if name == 'Species': 
        s_multi = True
        c_multi = False
    else:
        s_multi = False
        c_multi = True
        
    df = get_df(data)

    countries_choice = df['country'].unique().tolist()
    species_choice = df['species'].unique().tolist()

    return countries_choice, c_multi, species_choice, s_multi


# Update year options 
@app.callback(
    dash.dependencies.Output('start year','options'),
    dash.dependencies.Output('end year','options'),
    dash.dependencies.Input('dataset','value'),
    dash.dependencies.Input('species','value'),
    dash.dependencies.Input('country', 'value')
)
def update_year_dropdown(data, species, country): 

    df = get_df(data)

    # Determine types to filter df 
    if type(country) == str: 
        df = df[df['country'] == country]
    else: 
        df = df[df['country'].isin(country)]
    
    if type(species) == str: 
        df = df[df['species'] == species]
    else: 
        df = df[df['species'].isin(species)]

    df = df.sort_values(by=['year'])
    years = df['year'].unique()

    return years, years

# Update graph
@app.callback(
    dash.dependencies.Output('graph1','figure'),
    dash.dependencies.Input('country','value'),
    dash.dependencies.Input('species','value'),
    dash.dependencies.Input('start year', 'value'),
    dash.dependencies.Input('end year', 'value'),
    dash.dependencies.Input('dataset','value'),
    dash.dependencies.Input('plot','value')
)
def update_graph(country, species, start, end, data, plot):

    df = get_df(data)
    df = prep_df(df, country, species, start, end)

    if plot == 'stacked bar':
        fig = create_bar_plot(df, country, species)
    else:
        fig = create_scatter_plot(df, country, species)

    return(fig)

if __name__ == "__main__":
    app.run_server(debug=True)