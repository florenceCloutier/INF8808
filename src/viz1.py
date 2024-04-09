from helpers import Helper
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc


dict_pref = {
    'sous_genres' : ['trap','neo soul','tropical'],
    'artistes': ['Ed Sheeran','Metallica','Drake']
}

helper = Helper('./data/spotify_songs.csv')


def show_viz1():
    return html.Div(children=[
        html.Div(children=[
            html.H1('Voici votre profil', className='title-viz1'),
        ], className='header-viz1'),
        html.Div(children=[
            dcc.Graph(
                id='radar-chart-viz1',
                figure=user_preferences_chart(),
            )
        ], className='radar-chart-viz1'),
    ])

    
def user_preferences_chart():
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
