import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from urllib.parse import parse_qs, urlparse, unquote
from dash.dependencies import Input, Output, State
from viz1 import show_viz1
from viz2 import show_viz2
from viz3 import show_viz3
from viz4 import getRecommendationsForDecade
from user_profile import getUserProfilSubGenre
from methodology import getMethodologyComponent

import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = 'Spotify Song Recommender'

def show_user_preferences():
    return getUserProfilSubGenre()

def add_vertical_space():
    return html.Div(children=[html.Hr(), html.Div(style={'height': '100px'})])

def showVizualizations(dict_pref):
    return html.Div(children=[
    show_viz1(dict_pref),
    add_vertical_space(),
    show_viz3(dict_pref),
    add_vertical_space(),
    show_viz2(dict_pref),
    add_vertical_space(),
    getRecommendationsForDecade(2010, 2019, dict_pref),
    add_vertical_space(),
    getMethodologyComponent()
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('url', 'href')])
def display_page(pathname, href):
    # Parse the URL to get the query parameters
    parsed_url = urlparse(href)
    query_params = parse_qs(parsed_url.query)

    # Get the dict_pref query parameter
    dict_pref_str = query_params.get('dict_pref', [None])[0]
    if dict_pref_str is not None:
        dict_pref = json.loads(unquote(dict_pref_str))
    if pathname == '/userpreferences' or pathname == '/':
        return show_user_preferences()
    elif pathname == '/viz':        
        return showVizualizations(dict_pref)
    else:
        return "404 Page Error! Please select a link"
    
server = app.server
