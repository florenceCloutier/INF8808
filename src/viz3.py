import dash
from dash import State
import dash_html_components as html
from dash import callback, Input, Output
from dash.exceptions import PreventUpdate
from helpers import Helper


attributes = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

dict_pref = {
    'sous_genres' : ['trap','neo soul','tropical'],
    'artistes': ['Ed Sheeran','Metallica','Drake']
}

helper = Helper('../data/spotify_songs.csv')

def getTopSongs():
    helper = Helper('./data/spotify_songs.csv')
    recommendations_df, mean_pref_values = helper.generate_recommendations_df(dict_pref, recommendation_type='chansons')
    top_songs = recommendations_df['danceability'].head(10)
    return top_songs

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
    
    btn_styles[0]['background-color'] = '#1db954' if changed_id == 'btn-songs' else '#b3b3b3'
    btn_styles[1]['background-color'] = '#1db954' if changed_id == 'btn-artists' else '#b3b3b3'
    btn_styles[2]['background-color'] = '#1db954' if changed_id == 'btn-playlists' else '#b3b3b3'
    
    if changed_id == '':
        btn_styles[0]['background-color'] = '#1db954'
    
        
    return btn_styles

def show_buttons():
    return html.Div([
        html.Button('Chansons', id='btn-songs', n_clicks=0),
        html.Button('Artistes', id='btn-artists', n_clicks=0),
        html.Button('Playlists', id='btn-playlists', n_clicks=0)
        ],style={'display':'flex','justify-content':'center','align-items':'center'})


# TODO : Add a callback for the hover on the song
def show_top_songs():
    recommendations_df, mean_pref_values = helper.generate_recommendations_df(dict_pref, recommendation_type='chansons')
    top_songs = recommendations_df['track_name'].tolist()
    return html.Div([
        html.H2("Recommandations de chansons", className='top-title'),
        html.Ul([
            html.Li(song,
                    className='list',
                    id={'type':'li','index':idx}, 
                   ) for idx,song in enumerate(top_songs)
            ]) 
            ])


# TODO : Add a callback for the hover on the artist
def show_top_artists():
    recommendations_df, mean_pref_values = helper.generate_recommendations_df(dict_pref, recommendation_type='artistes')
    top_artists = recommendations_df['track_artist'].tolist()
    return html.Div([
        html.H2("Recommandations d'artistes", className='top-title'),
        html.Ul([
            html.Li(artist,
                    className='list',
                    id={'type':'li','index':idx}, 
                   ) for idx,artist in enumerate(top_artists)
            ]) 
        ])

# TODO : Add a callback for the hover on the playlist
def show_top_playlists():
    recommendations_df, mean_pref_values = helper.generate_recommendations_df(dict_pref, recommendation_type='playlist')
    top_playlists = recommendations_df['playlist_name'].tolist()
    return html.Div([
        html.H2("Recommandations de playlists", className='top-title'),
        html.Ul([
            html.Li(playlist,
                    className='list',
                    id={'type':'li','index':idx}) for idx,playlist in enumerate(top_playlists)
            ]) 
        ])

