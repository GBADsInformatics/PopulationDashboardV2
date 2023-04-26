import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from app import app
from layouts import layout, data_tab, graph_tab, metadata_tab, map_tab

###--------------Read in data-----------------------------------

eurostat = pd.read_csv('data/eurostat.csv')
faostat = pd.read_csv('data/faostat.csv')
faotier1 = pd.read_csv('data/faotier1.csv')
woah = pd.read_csv('data/oie.csv')
unfccc = pd.read_csv('data/unfccc.csv')

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
    
app.layout = layout.app_layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'active_tab')])
def render_content(tab):
    if tab == 'tab-0':
        return graph_tab.content
    elif tab == 'tab-1':
        return map_tab.content
    elif tab == 'tab-2':
       return data_tab.content
    elif tab == 'tab-3':
        return metadata_tab.metadata_content

# Organize options of selecting multiple
@app.callback(
    Output('country','multi'),
    Output('species','multi'),
    Input('tabs','active_tab'),
    Input('choice','value')
)
def update_multiples(at, choice):

    if choice == 'Species': 
        return(False, True)
    else: 
        return(True, False)
      
# Update country
@app.callback(
    Output('country','options'),
    Input('dataset','value')
)
def update_country_dd(data):

    df = get_df(data)
    
    country_options = df['country'].unique().tolist()

    return(country_options) 

# Update species 
@app.callback(
    Output('species','options'),
    [Input('country', 'value'),
     Input('dataset','value')]
)
def update_species_dd(country, data):

    # Get dataset 
    df = get_df(data)

    if country is None or len(country) < 1:
        print(f"User has selected no country options: {country}")

    elif type(country) == list and len(country) > 1:
        print(f"User has selected multiple country options: {country}")
        df = df[df['country'].isin(country)]

    elif type(country) == list and len(country) == 1: 
        print(f"User has selected a single country option: {country}")
        df = df[df['country'] == country]
    
    species_options = df['species'].unique().tolist()

    return(species_options) 

# Initialize dataset dropdown
@app.callback(
    Output('dataset','options'),
    Input('tabs','active_tab'),
)
def dataset_drop(at):

    dataset_options = ['eurostat','faostat','faotier1','woah','unfccc']

    return(dataset_options)

# Update year options 
@app.callback(
    Output('start year','options'),
    Output('end year','options'),
    Input('dataset','value'),
    Input('species','value'),
    Input('country', 'value')
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

# Update year option on map tab
@app.callback(
        Output('year','options'),
        Input('dataset','value'),
        Input('species','value'),
        Input('country','value')
)
def update_year_map(data, species, country): 

    df = get_df(data)
    df = df[df['country'].isin(country)]
    df = df[df['species'] == species]
    df = df.sort_values(by=['year'])
    years = df['year'].unique()
    return(years)

# Display metadata 
@app.callback(
    Output('metadata-table','data'),
    Input('dataset','value'),
    Input('tabs','active_tab')
)
def get_metadata(data, at):
    
    df = metadata_tab.get_metadata_df(data)

    return df.to_dict('records')

# Display graph
# Update graph
@app.callback(
    Output('graph1','figure'),
    Input('country','value'),
    Input('species','value'),
    Input('start year', 'value'),
    Input('end year', 'value'),
    Input('dataset','value'),
    Input('plot','value'))
def update_graph(country, species, start, end, data, plot, ):

    df = get_df(data)
    df = prep_df(df, country, species, start, end)

    if plot == 'stacked bar':
        fig = graph_tab.create_bar_plot(df, country, species)
    elif plot == 'scatter':
        fig = graph_tab.create_scatter_plot(df, country, species)
    else:
        print('map here')

    return(fig)

# Update data table 
@app.callback(
    Output('datatable','data'),
    Output('datatable','columns'),
    Input('dataset','value'),
    Input('country','value'), 
    Input('species','value'),
    Input('start year', 'value'),
    Input('end year', 'value'),
    )
def update_table(data, country, species, start, end):

    df = get_df(data)
    df = prep_df(df, country, species, start, end)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


if __name__ == '__main__':
    app.run_server(debug=True)
    app.config['suppress_callback_exceptions'] = True