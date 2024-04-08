import dash_html_components as html
import dash
from dash import callback, Input, Output
from dash import State
import helpers
import pandas as pd


helper = helpers.Helper("../data/spotify_songs.csv")

# TODO - Use the real genre list instead of this dummy one
# Sample list of music genres
genres = ["Rock", "Pop", "Jazz", "Hip Hop", "Electronic", "Classical"]


# Function that gets called in app.pys
def getUserProfilSubGenre():
    return html.Div([
                    html.Div(id='selected-genres'),
                    html.Div([
                        html.Button(genre, id={'type': 'genre-button', 'index': i}, n_clicks=0, className='genre-button', style={'margin': '5px'}) 
                        for i, genre in enumerate(genres)
                    ], style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)'}),
                    html.Div(id='hidden-div', style={'display': 'none'})
                ])

@callback(
    [Output('selected-genres', 'children'),
     Output('hidden-div', 'children')],
    [Input({'type': 'genre-button', 'index': i}, 'n_clicks') for i in range(len(genres))]
)

def update_selected_genres(*args):
    print(type(args))
    selected_genres_index = [1 if num % 2 == 1 else 0 for num in args]
    # Select genres where the corresponding index in output_list is 1
    selected_genres = [genre for genre, select in zip(genres, selected_genres_index) if select == 1]
    print(selected_genres)
    
    # TODO: implement this function
    #helper.get_artists_by_genre(genre)
    artists = selected_genres 
    
    # Dynamically add buttons based on selection
    artist_buttons = []
    for artist in artists:
        # Create a button for each artist
        button = html.Button(artist, id={'type': 'artist-button', 'index': artist}, n_clicks=0, className='artist-button', style={'margin': '5px'})
        artist_buttons.append(button)
    
    artist_div = html.Div(artist_buttons)

    # Return selected genres text and artist buttons
    return f"Selected Genres: {', '.join(selected_genres)}", artist_div
