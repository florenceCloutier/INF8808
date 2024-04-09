import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
from helpers import Helper

dict_pref = {
    'sous_genres' : ['trap','neo soul','tropical'],
    'artistes': ['Ed Sheeran','Metallica','Drake']
}

helper = Helper('./data/spotify_songs.csv')

def show_viz2():
    return html.Div(
        id="viz2-container", className="column", 
        children = [
            html.Div(
                id="viz2",
                children=[
                    getVisualisation2Component()
                ]
            )])
        
    
def getVisualisation2Component():
    return html.Div(className="column", children = [
            html.Div(className="title", children=[  
                html.H1("Vos compatibilités avec les différents genres musicaux", style={'textAlign': 'center', })
            ]),
            dcc.Graph(figure=getGenreCompatibilityComponent(), 
                  id='swarm-chart',
                  config=dict(
                      showTips=False,
                      showAxisDragHandles=False,
                      displayModeBar=False))
            ]
        )
    
    
def getGenreCompatibilityComponent():
    data = helper.generate_subgenre_similarity_df(dict_pref)
    df = pd.DataFrame(data)
    df = df.rename(columns={"playlist_subgenre": "Sous-genre"})
    
    colorMap = {
        'rock': '#00A36C',
        'pop': '#57C0F2',
        'rap': '#A8F2F2',
        'latin': '#57F28A',
        'r&b': '#578FF2',
        'edm': 'white',
    }
    
    fig = px.strip(df, x='similarity', color='playlist_genre',
                hover_data={'Sous-genre': True, 'playlist_genre': False, 'similarity': False},
                labels={'similarity': 'Similarity Level'}, color_discrete_map=colorMap)
    
    fig.update_traces({'marker':{'size': 40, 'line': {'width': 1, 'color': 'DarkSlateGrey'}}})
    
    fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
        })
    
    info = 'Passez votre curseur sur un marqueur pour plus d\'information'

    fig.update_layout(annotations=[dict(xref='paper',
                                    yref='paper',
                                    x=0.5, y=1.11,
                                    showarrow=False,
                                    text=info,
                                    font_color='white',
                                    font=dict(family="SpotifyFont, sans-serif", size=20))],
                      legend_title_text='Genre',
                      legend_title_font_color='white',
                      legend_font_color='white',
                      legend_font_size=12,
                      legend=dict(font=dict(family="SpotifyFont, sans-serif", size=20), orientation="v", yanchor="auto", y=1, xanchor="right", x=0),
                      xaxis_title="",
                      yaxis_title="",
                      xaxis=dict(showticklabels=True, visible=True),
                      yaxis=dict(visible=False),
                      margin=dict(l=200, r=200),
                      hoverlabel=dict(
                        font_size=16,
                        font_family="SpotifyFont, sans-serif"))
    
    min_range = df['similarity'].min()
    max_range = df['similarity'].max()
    
    div_range = (max_range - min_range) / 4
    margin = div_range / 5
    
    fig.update_xaxes(color='white', 
                     showgrid=False,
                     tickfont=dict(size=16, family="SpotifyFont, sans-serif"),
                     ticks='inside', 
                     ticklen=20,
                     tickvals=[min_range + margin, min_range + div_range + margin , min_range + 2 * div_range + margin, min_range + 3 * div_range + margin, max_range + margin],
                     ticktext=["Pas compatible",  "Peu compatible", "Moyennement compatible", "Compatible", "Pleinement compatible"],
                     range=[min_range - margin, max_range + 2 * margin],
                     showline=True,
                     linewidth=2)
    fig.update_yaxes(visible=False)
    
    return fig