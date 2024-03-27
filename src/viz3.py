import dash
from dash import State
import dash_html_components as html
from dash import callback, Input, Output
from dash.exceptions import PreventUpdate




top_songs = ["Chanson 1", "Chanson 2", "Chanson 3", "Chanson 4", "Chanson 5", "Chanson 6", "Chanson 7", "Chanson 8", "Chanson 9", "Chanson 10"]
top_artists = ["Artiste 1", "Artiste 2", "Artiste 3", "Artiste 4", "Artiste 5", "Artiste 6", "Artiste 7", "Artiste 8", "Artiste 9", "Artiste 10"]
top_playlists = ["Playlist 1", "Playlist 2", "Playlist 3", "Playlist 4", "Playlist 5", "Playlist 6", "Playlist 7", "Playlist 8", "Playlist 9", "Playlist 10"]


attributes = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']


@callback(
        Output('show_top_10', 'children'),
        [Input('btn-songs', 'n_clicks'),
        Input('btn-artists', 'n_clicks'),
        Input('btn-playlists', 'n_clicks')],
)
def show_top_10(btn_songs, btn_artists, btn_playlists):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn-songs' in changed_id:
        return show_top_songs()
    elif 'btn-artists' in changed_id:
        return show_top_artists()
    elif 'btn-playlists' in changed_id:
        return show_top_playlists()
    else:
        return show_top_songs()
   

@callback(
    [Output('btn-songs', 'style'), Output('btn-artists', 'style'), Output('btn-playlists', 'style')],
    [Input('btn-songs', 'n_clicks'),Input('btn-artists', 'n_clicks'),Input('btn-playlists', 'n_clicks')],
    [State('btn-songs', 'id'),State('btn-artists', 'id'),State('btn-playlists', 'id')]
)
def update_button_style(btn_songs_clicks, btn_artists_clicks, btn_playlists_clicks,btn_songs_id,btn_artists_id,btn_playlists_id):
    ctx = dash.callback_context
    changed_id = ctx.triggered[0]['prop_id'].split('.')[0]
    btn_styles = [{'font-size':30,'padding':20,'width':200},{'font-size':30,'padding':20,'width':200},{'font-size':30,'padding':20,'width':200}]

    if changed_id == 'btn-songs':
        btn_styles[0]['background-color'] = '#90D26D'
        btn_styles[1]['background-color'] = None
        btn_styles[2]['background-color'] = None
    elif changed_id == 'btn-artists':
        btn_styles[0]['background-color'] = None
        btn_styles[1]['background-color'] = '#90D26D'
        btn_styles[2]['background-color'] = None
    elif changed_id == 'btn-playlists':
        btn_styles[0]['background-color'] = None
        btn_styles[1]['background-color'] = None
        btn_styles[2]['background-color'] = '#90D26D'
    else:
        btn_styles[0]['background-color'] = '#90D26D'
        btn_styles[1]['background-color'] = None
        btn_styles[2]['background-color'] = None
    return btn_styles

def show_buttons():
    return html.Div([
        html.Button('Chansons', id='btn-songs', n_clicks=0),
        html.Button('Artistes', id='btn-artists', n_clicks=0),
        html.Button('Playlists', id='btn-playlists', n_clicks=0)
        ],style={'display':'flex','justify-content':'center','align-items':'center'})


# TODO : Add a callback for the hover on the song
def show_top_songs():
    return html.Div([
        html.H2("Recommandations de chansons"),
        html.Ul([
            html.Li(song, 
                    id={'type':'li','index':idx}, 
                    style={'font-size':30,'padding':20,'list-style-type':'none'}) for idx,song in enumerate(top_songs)
            ]) 
            ])


# TODO : Add a callback for the hover on the artist
def show_top_artists():
    return html.Div([
        html.H2("Recommandations d'artistes"),
        html.Ul([
            html.Li(artist,
                    id={'type':'li','index':idx}, 
                    style={'font-size':30,'padding':20,'list-style-type':'none'}) for idx,artist in enumerate(top_artists)
            ]) 
            ])

# TODO : Add a callback for the hover on the playlist
def show_top_playlists():
    return html.Div([
        html.H2("Recommandations de playlists"),
        html.Ul([
            html.Li(playlist, 
                     id={'type':'li','index':idx}, style={'font-size':30,'padding':20,'list-style-type':'none'}) for idx,playlist in enumerate(top_playlists)
            ]) 
            ])

