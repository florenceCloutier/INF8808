import dash_html_components as html
from dash import callback_context, dcc
from dash import ALL
import dash
from dash import callback, Input, Output
from dash import State
import helpers
import pandas as pd

helper = helpers.Helper("../data/spotify_songs.csv")

# TODO - Use the real genre list instead of this dummy one
# Sample list of music genres
genres = helper.generate_genres_list()
all_artist_list = helper.generate_artists_list()
# Function that gets called in app.pys
def getUserProfilSubGenre():
    return html.Div([
                    html.Div(id='selected-genres', style = {'display':'none'}),
                    html.Div(className="title", children=[
                        html.H1(['Sélectionnez vos genres préférez'], style={'margin-top': '15px', 'textAlign': 'center'})
                    ]),
                    html.Div([
                        html.Button(genre, id={'type': 'genre-button', 'index': i}, n_clicks=0, className='genre-button', style={'margin': '5px'}) 
                        for i, genre in enumerate(genres)
                    ], style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)'}),
                    
                    html.Div(className="select-genres", children=[
                        html.Button('Confirmation de la sélection', id='selection-button', n_clicks=0, style={'margin-top': '15px', 'textAlign': 'center'})  # New Selection button
                    ]),
                    html.Div(id='hidden-div'),#, style={'display': 'none'})
                    
                    ])

@callback(
    [Output('selected-genres', 'children'),
     Output({'type': 'genre-button', 'index': ALL}, 'style')],
    [Input({'type': 'genre-button', 'index': ALL}, 'n_clicks') ]
)
def update_selected_genres(n_clicks):
    print(n_clicks)
    global selected_genres
    selected_genres_index = [1 if (num % 2 == 1) else 0 for num in n_clicks]
    selected_genres = [genre for genre, select in zip(genres, selected_genres_index) if select == 1]
    
    button_styles = []
    for i, n_clicks in enumerate(n_clicks):
        button_style = {'margin': '5px'}
        if n_clicks and n_clicks % 2 == 1:
            button_style['background-color'] = 'green'
        button_styles.append(button_style)
    
    print(selected_genres)
    return f"Selected Genres: {', '.join(selected_genres)}", button_styles

@callback(
    Output('hidden-div', 'children'),
    [Input('selection-button', 'n_clicks')],
    prevent_initial_call=True
)
def generate_new_grid(n_clicks):
    print(n_clicks)
    print(selected_genres)
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    # TODO: Implement logic to extract artists based on genres
    global artists 
    artists = selected_genres

    artist_div = html.Div([
        html.Div(className="title", children=[
            html.H1(['Sélectionnez vos artistes favoris'], style={'margin-top': '15px', 'textAlign': 'center'})
        ]),
        html.Div(id='selected-artists', style = {'display':'none'}),
        html.Div([
            html.Button(artist, id={'type': 'artist-button', 'index': i}, n_clicks=0, className='artist-button',
                        style={'margin': '5px'})
            for i, artist in enumerate(artists)
        ], style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)'}),
        html.Div([
            dcc.Dropdown(all_artist_list, 'artists', id='artist-dropdown'),
            html.Div(id='dd-output-container')
        ]),
        html.Div(className="select-artists", children=[
                        html.Button('Confirmation de la sélection des artistes', id='selection-button-artist', n_clicks=0, style={'margin-top': '15px', 'textAlign': 'center'})  # New Selection button
                    ]),
        html.Div(id='artist-div')
    ])
    
    return artist_div

@callback(
    [Output('selected-artists', 'children'),
     Output({'type': 'artist-button', 'index': ALL}, 'style')],
    [Input({'type': 'artist-button', 'index': ALL}, 'n_clicks')]
)
def update_selected_artists(n_clicks):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    global selected_artists
    global selected_artists_search
    
    if selected_artists_search is None:
        selected_artists_search = []
    
    print(n_clicks)
    
    selected_artists_index = [1 if (num % 2 == 1) else 0 for num in n_clicks]
    selected_artists = [artist for artist, select in zip(artists, selected_artists_index) if select == 1]
    selected_artists.append(selected_artists_search)
    button_styles = []
    for i, n_clicks in enumerate(n_clicks):
        button_style = {'margin': '5px'}
        if n_clicks and n_clicks % 2 == 1:
            button_style['background-color'] = 'green'
        button_styles.append(button_style)
    
    return f"Selected Genres: {', '.join(selected_artists)}", button_styles

@callback(
    Output('artist-div', 'children'),
    [Input('selection-button-artist', 'n_clicks')],
    prevent_initial_call=True
)
def generate_profil_pref(n_clicks):
    print(n_clicks)
    print(selected_artists)
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    return 

@callback(
    Output('dd-output-container', 'children'),
    Input('artist-dropdown', 'value')
)
def update_output(value):
    global selected_artists_search
    if selected_artists_search is None:
        selected_artists_search = []
    selected_artists_search.append(value)
    return f'You have selected {value}'