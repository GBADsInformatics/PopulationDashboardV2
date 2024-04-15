import os
import dash
import plotly
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import json
from dash.exceptions import PreventUpdate
from datetime import datetime
from utils import newS3TicketLib as s3f
from utils import secure_rds as secure
from utils import rds_functions as rds

from app import app
from layouts import comments_section, layout, data_tab, graph_tab, metadata_tab, map_tab

# Access AWS Credentials and establish session
access, secret = s3f.get_keys()
s3_resource = s3f.credentials_resource ( access, secret )
s3_client = s3f.credentials_client ( access, secret )

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
      
# Update all dropdowns
@app.callback(
    Output('country','options'),
    Output('species','options'),
    Output('start year','options'),
    Output('end year','options'),
    Input('dataset','value'),
)
def update_all_dd(data):

    df = get_df(data)
    
    country_options = df['country'].unique().tolist()
    
    species_options = df['species'].unique().tolist()

    df = df.sort_values(by=['year'])
    
    years = df['year'].unique()

    return(country_options, species_options, years, years) 

# Update species 
# @app.callback(
#     Output('species','options'),
#     [Input('country', 'value'),
#      Input('dataset','value')]
# )
# def update_species_dd(country, data):

    # Get dataset 
    # df = get_df(data)

    # # Set default 
    # if country == str:
    #     print(f"User has selected no country options: {country}")

    # elif type(country) == list and len(country) > 1:
    #     df = df[df['country'].isin(country)]

    # elif type(country) == list: 
    #     df = df.loc[df['country'] == country]
    
    # species_options = df['species'].unique().tolist()

    # return(species_options) 

# Initialize dataset dropdown
@app.callback(
    Output('dataset','options'),
    Input('tabs','active_tab'),
)
def dataset_drop(at):

    dataset_options = ['eurostat','faostat','faotier1','woah','unfccc']

    return(dataset_options)

# Update year options 
# @app.callback(
#     Output('start year','options'),
#     Output('end year','options'),
#     Input('dataset','value'),
# )
# def update_year_dropdown(data): 

#     df = get_df(data)

    # Determine types to filter df 
    # if type(country) == str: 
    #     df = df[df['country'] == country]
    #     df = df[df['species'].isin(species)]
    # else: 
    #     df = df[df['species'] == species]
    #     df = df[df['country'].isin(country)]

    # df = df.sort_values(by=['year'])
    # years = df['year'].unique()

    # return years, years

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
def update_graph(country, species, start, end, data, plot):

    if type(country) == list and type(species) == list:
        raise PreventUpdate

    df = get_df(data)
    df = prep_df(df, country, species, start, end)

    if plot == 'stacked bar':
        fig = graph_tab.create_bar_plot(df, country, species)
    elif plot == 'scatter line':
        fig = graph_tab.create_scatter_plot(df, country, species)

    return(fig)

###--------------Comments Section-----------------------------------
# comment table tabs
@app.callback(
        Output('comment-tabs-content', 'children'),
        Input('choice', 'value'),
        Input('dataset', 'value'),
        Input('country', 'value'),
        [Input('comment-tabs', 'active_tab')]
)
def render_content(choice, dataset, country, tab):
    if tab == 'tab-0':
        #get new comments
        conn = secure.connect_public()
        cur = conn.cursor()
        fieldstring = "created,tablename,subject,message,name,email,ispublic,reviewer"
        #change to not include time
        querystring = f"dashboard='population_dashboard' AND tablename LIKE '{choice} {dataset} {country}%'"
        querystr = rds.setQuery ("gbads_comments", fieldstring, querystring, "")
        comments = rds.execute ( cur, querystr )
        conn.close()

        child = []
        for row in comments:
            child.append(html.Div(children=[
                html.H5(row[4] if row[6] == True else 'Anonymous', style=comments_section.commentHeading),
                html.H6(row[1], style=comments_section.commentSubheading),
                html.H6(row[0][:-9], style=comments_section.commentDate),
                html.H6(row[2]),
                html.H6(row[3]),
            ],
            style = comments_section.divBorder
            ))
            child.append(html.Br())
        return html.Div(children=
            [
                html.Div(id='comments', children=child)
            ],
            style=comments_section.COMMENT_STYLE,
        )
    elif tab == 'tab-1':
        return comments_section.comment_add

# Comment table changing in add comment Tab
@app.callback(
    Output('comments-table','value'),
    Input('choice', 'value'),
    Input('dataset', 'value'),
    Input('country', 'value'),
    Input('species', 'value'),
    Input('start year', 'value'),
    Input('end year', 'value'),
    Input('plot', 'value'),
)
def update_comment_table(choice, dataset, country, species, start, end, plot):
    species.sort()
    species_str = ','.join(species)
    return f'{choice} {dataset} {country} {species_str} {start}-{end} {plot}'

# Comment Submition in add comment tab
@app.callback(
        Output('com', 'children'),
        Output('comments-subject', 'value'),
        Output('comments-message', 'value'),
        Output('comments-name', 'value'),
        Output('comments-email', 'value'),
        Output('comments-isPublic', 'value'),
        Input('comments-button', 'n_clicks'),
        State('comments-table', 'value'),
        State('comments-subject', 'value'),
        State('comments-message', 'value'),
        State('comments-name', 'value'),
        State('comments-email', 'value'),
        State('comments-isPublic', 'value'),
)
def submit_comment(n_clicks, table, subject, message, name, email, isPublic):
    if subject == '':
        return f'Subject is required', subject, message, name, email, isPublic;
    if message == '':
        return f'Message is required', subject, message, name, email, isPublic;
    if n_clicks > 0:
        # create comment file
        created = datetime.now()
        comment = {
            "created": f'{created}',
            "dashboard": 'population_dashboard',
            "table": table,
            "subject": subject,
            "message": message,
            "name": name,
            "email": email,
            "isPublic": True if isPublic == "Yes" else False,
            "reviewer": ''
        }
        filename = f'{created}.json'
        with open(filename, "w") as outfile:
            json.dump(comment, outfile)
        # upload comment file
        ret = s3f.s3Upload ( s3_resource, 'gbads-comments', filename, f"underreview/{filename}" )
        #delete comment file
        os.remove(filename)
        if ( ret == -1 ):
            return f'Error: Unable to submit comment', '', '', '', '', 'No';
        return f'Submitted Successfully', '', '', '', '', 'No';
    return f'', '', '', '', '', 'No';

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

# Update map
# Update year option on map tab
@app.callback(
    Output('species-map','options'),
    Output('year-map','options'),
    Input('dataset','value'),
)
def update_species_map(data): 

    df = get_df(data)
    
    species = df['species'].unique()
    df = df.sort_values(by=['year'])
    year = df['year'].unique()

    return(species, year)

@app.callback(
    Output('map','figure'),
    Input('dataset','value'),
    Input('species-map','value'),
    Input('year-map', 'value'),
    )
def update_map(data, species, year):

    df = get_df(data)
    merged_df = df.loc[df['year'] == year]
    merged_df = merged_df.loc[merged_df['species'] == species]

    fig = map_tab.create_map(merged_df, data, species, year)

    return(fig)

if __name__ == '__main__':
    app.run_server(debug=True)
    app.config['suppress_callback_exceptions'] = True

# return the wsgi app
def returnApp():
    """
    This function is used to create the app and return it to waitress in the docker container
    """
    # If BASE_URL is set, use DispatcherMiddleware to serve the app from that path
    if 'BASE_URL' in os.environ:
        from flask import Flask
        from werkzeug.middleware.dispatcher import DispatcherMiddleware
        app.wsgi_app = DispatcherMiddleware(Flask('dummy_app'), {
            os.environ['BASE_URL']: app.server
        })
        # Added redirect to new path
        @app.wsgi_app.app.route('/')
        def redirect_to_dashboard():
            from flask import redirect
            return redirect(os.environ['BASE_URL'])
        return app.wsgi_app

    # If no BASE_URL is set, just return the app server
    return app.server