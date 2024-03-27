import dash_html_components as html
from dash import callback, Input, Output
import dash



top_songs = ["Chanson 1", "Chanson 2", "Chanson 3", "Chanson 4", "Chanson 5", "Chanson 6", "Chanson 7", "Chanson 8", "Chanson 9", "Chanson 10"]
top_artists = ["Artiste 1", "Artiste 2", "Artiste 3", "Artiste 4", "Artiste 5", "Artiste 6", "Artiste 7", "Artiste 8", "Artiste 9", "Artiste 10"]
top_playlists = ["Playlist 1", "Playlist 2", "Playlist 3", "Playlist 4", "Playlist 5", "Playlist 6", "Playlist 7", "Playlist 8", "Playlist 9", "Playlist 10"]


attributes = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

# def show_visualization():
#     return html.Div([
#         show_buttons(),
#         show_top_10()
#         ])

@callback(
        Output('show_top_10', 'children'),
        [Input('btn-songs', 'n_clicks'),
        Input('btn-artists', 'n_clicks'),
        Input('btn-playlists', 'n_clicks')]
)
def show_top_10(btn_songs, btn_artists, btn_playlists):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)
    if 'btn-songs' in changed_id:
        return show_top_songs()
    elif 'btn-artists' in changed_id:
        return show_top_artists()
    elif 'btn-playlists' in changed_id:
        return show_top_playlists()
    else:
        return show_top_songs()
   

def show_buttons():
    return html.Div([
        html.Button('Chansons', id='btn-songs', n_clicks=0, style={'font-size':30,'padding':20,'width':200}),
        html.Button('Artistes', id='btn-artists', n_clicks=0, style={'font-size':30,'padding':20,'width':200}),
        html.Button('Playlists', id='btn-playlists', n_clicks=0, style={'font-size':30,'padding':20,'width':200})
        ],style={'display':'flex','justify-content':'center','align-items':'center'})


def show_top_songs():
    return html.Div([
        html.H2("Recommandations de chansons"),
        html.Ul([
            html.Li(song, 
                    id={'type':'li','index':idx}, 
                    style={'font-size':30,'padding':20,'list-style-type':'none'}) for idx,song in enumerate(top_songs)
            ]) 
            ])



def show_top_artists():
    return html.Div([
        html.H2("Recommandations d'artistes"),
        html.Ul([
            html.Li(artist, style={'font-size':30,'padding':20,'list-style-type':'none'}) for artist in top_artists
            ]) 
            ])

def show_top_playlists():
    return html.Div([
        html.H2("Recommandations de playlists"),
        html.Ul([
            html.Li(playlist, style={'font-size':30,'padding':20,'list-style-type':'none'}) for playlist in top_playlists
            ]) 
            ])

