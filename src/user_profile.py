import dash_html_components as html
from dash import callback_context, dcc
from dash import ALL
import dash
from dash import callback, Input, Output
from dash import State
import helpers
import pandas as pd

helper = helpers.Helper("../data/spotify_songs.csv")
#selected_artists = []
#selected_genres = []
#global selected_artists_search

# TODO - Use the real genre list instead of this dummy one
# Sample list of music genres
genres = helper.generate_genres_list()
all_artist_list = helper.generate_artists_list()
# Function that gets called in app.pys
def getUserProfilSubGenre():
    return html.Div(children = [
                    html.Div(id="profil-title-text",className="title", children=[
                        html.H1(['Création de votre profil'], style={'margin-top': '15px', 'textAlign': 'center'})
                    ]),
                    html.Div(id='selected-genres', style = {'display':'none'}),
                    html.Div(className="title", children=[
                        html.H2(['Sélectionnez vos genres préférez:'], style={'textAlign': 'center'})
                    ]),
                    html.Div([
                        html.Div([
                            html.Button(genre, id={'type': 'genre-button', 'index': i}, 
                                        n_clicks=0, 
                                        className='genre-button',
                                        style={'margin': '30px'},
                                        ) 
                                        for i, genre in enumerate(genres)
                        ], className='divBorder', style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)'}),
                    ]),
                    html.Div(className="select-genres", children=[
                        html.Button('Confirmation de la sélection', className ="next-step-button",id='selection-button', n_clicks=0, style={'margin-top': '15px', 'textAlign': 'center','background-color':'#b3b3b3'})  # New Selection button
                    ], style={'display': 'grid', 'grid-template-columns': 'repeat(1, 1fr)'}),
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
            button_style['background-color'] = '#1db954'
        button_styles.append(button_style)
    
    print(selected_genres)
    return f"Selected Genres: {', '.join(selected_genres)}", button_styles

@callback(
    Output('hidden-div', 'children'),
    [Input('selection-button', 'n_clicks')],
    prevent_initial_call=True
)
def generate_new_grid(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    # TODO: Implement logic to extract artists based on genres
    global artists 
    global selected_artists_search
    selected_artists_search = []
    
    artists = helper.generate_sample_artists_from_genres(selected_genres)
    #artists = selected_genres

    artist_div = html.Div([
        html.Div(className="title", children=[
            html.H2(['Sélectionnez vos artistes favoris'], style={'margin-top': '15px', 'textAlign': 'center'})
        ]),
        html.Div(id='selected-artists', style = {'display':'none'}),
        html.Div(className="title", children=[
            html.H4(['Voici quelques artistes que vous pourriez aimer selon les genres sélectionnés'], style={'margin-top': '5px','margin-bottom': '5px', 'textAlign': 'center'})
        ]),
        html.Div([
            html.Button(artist, id={'type': 'artist-button', 'index': i}, n_clicks=0, className='artist-button',
                        style={'margin': '5px'})
            for i, artist in enumerate(artists)
        ], className='divBorder', style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)'}),
        html.Div(className="title", children=[
            html.H4(["Chercher d'autres artistes favoris"], style={'margin-top': '5px','margin-bottom': '5px', 'textAlign': 'center'})
        ]),
        html.Div([
            dcc.Dropdown(all_artist_list, 'artists', id='artist-dropdown'),
            html.Div(id='dd-output-container')
        ], className='dropdownBorder'),
        html.Div(className="select-artists", children=[
                        html.Button("Confirmation de la sélection d'artistes", className ="next-step-button", id='selection-button-artist', n_clicks=0, style={'margin-top': '15px', 'textAlign': 'center','background-color':'#b3b3b3'})  # New Selection button
                    ], style={'display': 'grid', 'grid-template-columns': 'repeat(1, 1fr)'}),
        
        html.Div(id='artist-div')
    ])
    
    return artist_div

@callback(
    [Output('selected-artists', 'children'),
     Output({'type': 'artist-button', 'index': ALL}, 'style')],
    [Input({'type': 'artist-button', 'index': ALL}, 'n_clicks')]
)
def update_selected_artists(n_clicks):
    global selected_artists
    
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    print(n_clicks)
    selected_artists_index = [1 if (num % 2 == 1) else 0 for num in n_clicks]
    selected_artists = [artist for artist, select in zip(artists, selected_artists_index) if select == 1]
    print(selected_artists)
    
    #selected_artists.append(selected_artists_search)
    button_styles = []
    for i, n_clicks in enumerate(n_clicks):
        button_style = {'margin': '5px'}
        if n_clicks and n_clicks % 2 == 1:
            button_style['background-color'] = '#1db954'
        button_styles.append(button_style)
    
    return f"Selected Genres: {', '.join(selected_artists)}", button_styles

@callback(
    Output('dd-output-container', 'children'),
    Input('artist-dropdown', 'value')
)
def update_output(value):
    global selected_artists_search
    if value not in selected_artists_search:
        selected_artists_search.append(value)
    print(selected_artists_search)
    
    selected_artists_search_str = ', '.join(selected_artists_search[1:])
    if (len(selected_artists_search) > 1):
        return html.Div([
            html.P(f'Voici votre sélection:  {selected_artists_search_str}',style={'color': 'white', 'font':'SpotifyFont'})])
    else:
        return
    

@callback(
    Output('artist-div', 'children'),
    [Input('selection-button-artist', 'n_clicks')],
    prevent_initial_call=True
)
def generate_profil_pref(n_clicks):
    
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    print(n_clicks)
    print(selected_artists)
    print(selected_artists_search[1:])
    final_artist_list = selected_artists + selected_artists_search[1:]
    user_pref = helper.generate_profil_attributes(final_artist_list, selected_genres)
    print(user_pref)
    return user_pref