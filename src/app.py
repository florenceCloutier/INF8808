import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


from viz3 import show_buttons, show_top_songs, show_top_artists, show_top_playlists

import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = 'Spotify Song Recommender'



# Define layout
app.layout = html.Div([
    show_buttons(),
    html.Div(id='show_top_10')
])

