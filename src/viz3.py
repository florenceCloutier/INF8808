import dash
from dash import State
import dash_html_components as html
from dash import callback, Input, Output, ALL
import plotly.graph_objects as go
import json
import dash_core_components as dcc
from helpers import Helper

helper = Helper('./data/spotify_songs.csv')

dict_pref_cache = None

def show_viz3(dict_pref):
    
    global dict_pref_cache
    dict_pref_cache = None
    if dict_pref_cache is None:
        dict_pref_cache = dict_pref
    
    return html.Div(children=[
        show_buttons(),
        html.Div(children=[
            html.Div(id='show_top_10'),
            html.Div(id='btn-clicked-style'),
        ],style={'width':'30%','display':'inline-block'}),
       
       html.Div(children=[
            dcc.Graph(
            id='radar-chart',
            figure=user_preferences_chart(dict_pref),
        )
        ],style={'width':'70%','display':'inline-block','margin-bottom':'100px',}),
       
    ])

@callback(
        Output('show_top_10', 'children'),
        [Input('btn-songs', 'n_clicks'),
        Input('btn-artists', 'n_clicks'),
        Input('btn-playlists', 'n_clicks')],
)
def show_top_10(btn_songs, btn_artists, btn_playlists):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    global dict_pref_cache
    if 'btn-songs' in changed_id:
        return show_top_songs(dict_pref_cache)
    elif 'btn-artists' in changed_id:
        return show_top_artists(dict_pref_cache)
    elif 'btn-playlists' in changed_id:
        return show_top_playlists(dict_pref_cache)
    else:
        return show_top_songs(dict_pref_cache)
   

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
        html.Button('Chansons', id='btn-songs', n_clicks=0,className='buttons-viz3'),
        html.Button('Artistes', id='btn-artists', n_clicks=0,className='buttons-viz3'),
        html.Button('Playlists', id='btn-playlists', n_clicks=0,className='buttons-viz3')
        ],className='buttons-viz3')


def show_top_songs(dict_pref):
    recommendations_df, mean_pref_values = helper.generate_recommendations_df(dict_pref, recommendation_type='chansons')
    top_songs = recommendations_df['track_name'].tolist()
    return html.Div([
        html.H2("Recommandations de chansons", className='top-title'),
        html.Ul([
            html.Li(song,
                    className='list',
                    id={'type':'chansons','index':idx},
                    style={'position':'relative'},
                    **{'data-index':idx}) for idx,song in enumerate(top_songs)
            ],className='hover-highlight') 
        ])
    

@callback(
    Output({'type': 'chansons', 'index': ALL}, 'style'),
    [Input({'type': 'chansons', 'index': ALL}, 'n_clicks')]
)
def update_playlist_style(n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    index = json.loads(changed_id.split('.')[0])['index'] if changed_id != '.' else 0
    return [{'position':'relative', 'background-color': '#1db954' if i == index else 'transparent'} for i in range(len(n_clicks))]

def show_top_artists(dict_pref):
    recommendations_df, mean_pref_values = helper.generate_recommendations_df(dict_pref, recommendation_type='artistes')
    top_artists = recommendations_df['track_artist'].tolist()
   
    return html.Div([
        html.H2("Recommandations d'artistes", className='top-title'),
        html.Ul([
            html.Li(artist,
                    className='list',
                    id={'type':'artistes','index':idx},
                    style={'position':'relative'},
                    **{'data-index':idx}) for idx,artist in enumerate(top_artists)
            ],className='hover-highlight') 
        ])
    
@callback(
    Output({'type': 'artistes', 'index': ALL}, 'style'),
    [Input({'type': 'artistes', 'index': ALL}, 'n_clicks')]
)
def update_playlist_style(n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    index = json.loads(changed_id.split('.')[0])['index'] if changed_id != '.' else 0
    return [{'position':'relative', 'background-color': '#1db954' if i == index else 'transparent'} for i in range(len(n_clicks))]


def show_top_playlists(dict_pref):
    recommendations_df, mean_pref_values = helper.generate_recommendations_df(dict_pref, recommendation_type='playlist')
    top_playlists = recommendations_df['playlist_name'].tolist()
    
    return html.Div([
        html.H2("Recommandations de playlists", className='top-title'),
        html.Ul(id='playlist-list',children = [
            html.Li(playlist,
                    className='list',
                    id={'type':'playlist','index':idx},
                    style={'position':'relative'},
                    **{'data-index':idx}) for idx,playlist in enumerate(top_playlists)
            ],className='hover-highlight') 
        ])
    

@callback(
    Output({'type': 'playlist', 'index': ALL}, 'style'),
    [Input({'type': 'playlist', 'index': ALL}, 'n_clicks')]
)
def update_playlist_style(n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    index = json.loads(changed_id.split('.')[0])['index'] if changed_id != '.' else 0
    return [{'position':'relative', 'background-color': '#1db954' if i == index else 'transparent'} for i in range(len(n_clicks))]
    
    
@callback(
    Output('radar-chart', 'figure'),
    [Input({'type': 'chansons', 'index': ALL}, 'n_clicks'),
     Input({'type': 'artistes', 'index': ALL}, 'n_clicks'),
     Input({'type': 'playlist', 'index': ALL}, 'n_clicks'),]
)
def update_radar_chart(n_clicks_chansons, n_clicks_artistes, n_clicks_playlists):
    ctx = dash.callback_context
    global dict_pref_cache
    if not ctx.triggered:
        return user_preferences_chart(dict_pref_cache)
    
    prop_id = ctx.triggered[0]['prop_id']
    
    type = json.loads(prop_id.split('.')[0])['type']
    selected_index = json.loads(prop_id.split('.')[0])['index']

    recommendations_df, _ = helper.generate_recommendations_df(dict_pref_cache, recommendation_type=type)

    data = recommendations_df.iloc[selected_index]
    data_criterias  = data[3:]if type == 'chansons' else data[1:]
   
    name = data['track_name'] if type == 'chansons' else data['track_artist'] if type == 'artistes' else data['playlist_name']
    
    real_values_data = helper.get_initial_values_by_type(name,type)
    
    real_values_data_criterias = real_values_data.iloc[0][3:] if type == 'chansons' else real_values_data.iloc[0]
    
    values_and_desriptions = [(i, j) for i, j in zip(real_values_data_criterias, helper.descriptions)]
  

    fig = user_preferences_chart(dict_pref_cache)
    
    fig.add_trace(go.Scatterpolar(
        r=data_criterias,
        theta=helper.criterias,
        customdata=values_and_desriptions,
        fill='tonext',
        hovertemplate=get_hover_template(),
        name=data['track_name'] if type == 'chansons' else data['track_artist'] if type == 'artistes' else data['playlist_name'],
        line = dict(color='#1db954')
    ))


    return fig
    
    
def user_preferences_chart(dict_pref):
    fig = go.Figure()
    user_pref_dict = helper.generate_user_preferences_dict(dict_pref)
    user_pref_real = helper.generate_real_user_preferences_dict(dict_pref)
    
    values_and_desriptions = [(i, j) for i, j in zip(list(user_pref_real.values()), helper.descriptions)]
    
    fig.add_trace(go.Scatterpolar(
        r=list(user_pref_dict.values()),
        customdata=values_and_desriptions,
        theta=helper.criterias,
        fill='tonext',
        name='Vos préférences',
        hovertemplate=get_hover_template(),
        line = dict(color='#e22128')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
            ),
            angularaxis=dict(
                color='white',
                tickfont=dict(
                    family='SpotifyFont',
                    size=20, 
                    color='white'
                )
            )),
        showlegend=True,
        legend=dict(
            font=dict(
                color='white',
                family='SpotifyFont',
                size=15
            )
        ),
        paper_bgcolor='#191414',
        
    )
    return fig


def get_hover_template():
    theta = '<b style="font-family: SpotifyFont">Attribut musical: %{theta}</b><br>'
    value = '<b style="font-family: SpotifyFont">Valeur: %{customdata[0]:.4f}</b><br>'
    description = '<b style="font-family: SpotifyFont">Description: %{customdata[1]}</b><br>'
    hover_template = theta + description +value + '<extra></extra>'
    return hover_template
