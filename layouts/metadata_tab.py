import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash import dash_table
from layouts import layout
import pandas as pd

def get_metadata_df(choice): 

    if choice == 'eurostat': 
        return(m_eurostat)
    elif choice == 'faostat':
        return(m_faostat)
    elif choice == 'faotier1': 
        return(m_faotier1)
    elif choice == 'woah':
        return(m_woah)
    elif choice == 'unfccc':
        return(m_unfccc)
    
###--------------Read in metadata-----------------------------------
m_eurostat = pd.read_csv('data/m_eurostat.csv')
m_faostat = pd.read_csv('data/m_faostat.csv')
m_faotier1 = pd.read_csv('data/m_faotier1.csv')
m_woah = pd.read_csv('data/m_oie.csv')
m_unfccc = pd.read_csv('data/m_unfccc.csv')

table = html.Div([
    html.P("Select a dataset on the left sidebar to view the metadata."),
    dash_table.DataTable(
            id='metadata-table',
            export_format='csv',
            style_cell={'textAlign': 'left', 'font-family':'sans-serif'},
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_data={
                'color': 'black',
            }
)])

metadata_content = dbc.Row(
    [
        dbc.Col(layout.sidebar_metadata, 
                xs=dict(order=1, size=12),
                sm=dict(order=1, size=3)
                ),
        dbc.Col(table,
                xs=dict(order=2, size=12),
                sm=dict(order=2, size='auto'))
    ], className='root-container'
)
