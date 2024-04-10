import dash
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


app.layout = html.Div(children=[
    show_viz1(dict_pref),
    show_viz2(dict_pref),
    show_viz3(dict_pref),
    getRecommendationsForDecade(2010, 2019, dict_pref)
])

server = app.server
