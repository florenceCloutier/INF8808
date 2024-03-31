import json

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

from create_profil import create_button_grid
import helpers

import create_profil

app = dash.Dash(__name__)
app.title = 'Spotify Song Recommender'

app.layout = html.Div([
    create_profil.create_button_grid(),
    html.Div(id='selected-genres-output'),
    html.Button('Submit', id='submit-button', n_clicks=0)
])

# Registering both callbacks
update_selected_genres = create_profil.update_selected_genres_callback(app)
reset_selected_genres = create_profil.reset_selected_genres_callback(app)


if __name__ == '__main__':
    app.run_server(debug=True)