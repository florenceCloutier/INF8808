import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from urllib.parse import parse_qs, urlparse
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


def show_user_preferences():
    return html.Div(children=[
        html.H1('User Preferences'),
        html.Div(children=[
            html.H3('Sous Genres'),
            html.P(dict_pref['sous_genres']),
            html.H3('Artistes'),
            html.P(dict_pref['artistes']),
            dcc.Link('Go to vizualizations', href='/viz?dict_pref=' + json.dumps(dict_pref))
        ])
    ])

def showVizualizations(dict_pref):
    return html.Div(children=[
    dcc.Link('Go back to user preferences', href='/userpreferences'),
    show_viz1(dict_pref),
    show_viz2(dict_pref),
    show_viz3(dict_pref),
    getRecommendationsForDecade(2010, 2019, dict_pref)
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
        dict_pref = json.loads(dict_pref_str)
    if pathname == '/userpreferences' or pathname == '/':
        return show_user_preferences()
    elif pathname == '/viz':
        return showVizualizations(dict_pref)
    else:
        return "404 Page Error! Please select a link"
    
server = app.server
