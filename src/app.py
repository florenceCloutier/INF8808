import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from viz1 import show_viz1
from viz2 import show_viz2
from viz3 import show_viz3
from viz4 import getRecommendationsForDecade

dict_pref = {
    'sous_genres' : ['trap','neo soul','tropical'],
    'artistes': ['Ed Sheeran','Metallica','Drake']
}

import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = 'Spotify Song Recommender'

def showVizualizations(dict_pref):
    return html.Div(children=[
    dcc.Link('Go back to user preferences', href='/userpreferences'),
    show_viz1(dict_pref),
    show_viz2(dict_pref),
    show_viz3(dict_pref),
    getRecommendationsForDecade(2010, 2019, dict_pref)
])
    
def show_user_preferences():
    return html.Div(children=[
        html.H1('User Preferences'),
        html.Div(children=[
            html.H3('Sous Genres'),
            html.P(dict_pref['sous_genres']),
            html.H3('Artistes'),
            html.P(dict_pref['artistes']),
            dcc.Link('Go to vizualizations', href='/viz')
        ])
    ])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/viz':
        return showVizualizations(dict_pref)
    elif pathname == '/userpreferences':
        return show_user_preferences()
    else:
        return "404 Page Error! Please select a link"

server = app.server

server = app.server
