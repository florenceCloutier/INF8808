import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


from viz3 import show_buttons, user_preferences_chart

import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = 'Spotify Song Recommender'


app.layout = html.Div(children=[
    show_buttons(),
    html.Div(children=[
        html.Div(id='show_top_10'),
        html.Div(id='btn-clicked-style'),
    ],style={'width':'40%','display':'inline-block'}),
   
   html.Div(children=[
        dcc.Graph(
        id='radar-chart',
        figure=user_preferences_chart(),
    )
    ],style={'width':'50%','display':'inline-block','margin-bottom':'100px'}),
   
])

