import json

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

from viz4 import getRecommendationsForDecade

app = dash.Dash(__name__)
app.title = 'Spotify Song Recommender'

app.layout = html.Div(getRecommendationsForDecade(2010, 2019))