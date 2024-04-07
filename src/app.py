import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
from viz1 import show_viz1
from viz3 import show_viz3

import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = 'Spotify Song Recommender'


app.layout = html.Div(children=[
    show_viz1(),
    show_viz3()
   
])

