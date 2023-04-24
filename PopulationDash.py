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
import graph_helpers as gh
from layout import app_layout
import graph_tab 
import data_tab

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.LUX])

# Import layout from layout file 
app.layout = app_layout

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


###--------------Call backs------------------------------------

# Initialize dataset dropdown
@app.callback(
    dash.dependencies.Output('dataset','options'),
    dash.dependencies.Input('choice','value')
)
def dataset_drop(name):
    
    dataset_options = ['eurostat','faostat','faotier1','woah','unfccc']

    return(dataset_options)

@app.callback(
        dash.dependencies.Output('page-content', 'children'),
        dash.dependencies.Output('plot','disabled'),
        dash.dependencies.Input('tabs','active_tab')
)
def switch_tab(at):
    if at == "tab-0":
        return graph_tab.tab1_content, False
    elif at == "tab-1": 
        return data_tab.table, True
    return("Metadata here")
    # return html.P("This shouldn't ever be displayed...")

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
        df = df[df['species'].isin(species)]
    else: 
        df = df[df['species'] == species]
        df = df[df['country'].isin(country)]

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
    dash.dependencies.Input('plot','value'))
def update_graph(country, species, start, end, data, plot, ):

    df = get_df(data)
    df = prep_df(df, country, species, start, end)

    if plot == 'stacked bar':
        fig = gh.create_bar_plot(df, country, species)
    elif plot == 'scatter':
        fig = gh.create_scatter_plot(df, country, species)
    else:
        print('map here')

    return(fig)

# Update data table 
@app.callback(
    dash.dependencies.Output('datatable','data'),
    dash.dependencies.Output('datatable','columns'),
    dash.dependencies.Input('dataset','value'),
    dash.dependencies.Input('country','value'), 
    dash.dependencies.Input('species','value'),
    dash.dependencies.Input('start year', 'value'),
    dash.dependencies.Input('end year', 'value'),
    )
def update_table(data, country, species, start, end):

    df = get_df(data)
    df = prep_df(df, country, species, start, end)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


if __name__ == "__main__":
    app.run_server(debug=True)
