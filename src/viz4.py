import dash_html_components as html
import dash
from dash import callback, Input, Output
from dash import State

@callback(
    Output('viz4-container', 'children'),
    [Input('generate-decade-button', 'n_clicks')],
    [State('generate-decade-button', 'value')]
)
def generate_decade_recommendations(n_clicks, value):
    if n_clicks is None:
        return dash.no_update

    start_year, end_year = value.split('-')
    start_year = int(start_year)
    end_year = int(end_year)
    
    if end_year < 1970 or end_year > 2019:
        return dash.no_update
    
    return getRecommendationsForDecade(start_year, end_year)

tmpTopSongs = ["Bohemian Rhapsody", "Stairway to Heaven", "Hotel California", "Imagine", "Smells Like Teen Spirit", "What's Going On", "One", "Comfortably Numb", "Like a Rolling Stone", "Hey Jude"]
            # "Bohemian Rhapsody", "Stairway to Heaven", "Hotel California", "Imagine", "Smells Like Teen Spirit", "What's Going On", "One", "Comfortably Numb", "Like a Rolling Stone", "Hey Jude",
            # "Let It Be", "Yesterday", "A Day in the Life", "Hallelujah", "Blowin' in the Wind", "The Times They Are a-Changin'", "Sweet Child o' Mine", "Under the Bridge", "Californication", "Lose Yourself",
            # "The Real Slim Shady", "Without Me", "In the End", "Numb", "Faint", "Breaking the Habit", "Somewhere I Belong", "Crawling", "One Step Closer", "A Place for My Head",
            # "Forgotten", "With You", "Runaway", "By Myself", "Don't Stay", "Go", "Lying from You", "Hit the Floor", "Easier to Run", "Faint"]

tmpTopArtists = ["Artiste A", "Artiste B", "Artiste C", "Artiste D", "Artiste E"]
tmpTopGenres = ["Genre A", "Genre B", "Genre C", "Genre D", "Genre E"]

years = [2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010,
         2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000,
         1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990,
         1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980,
         1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970,]

explorationString1 = "Exploration de vos potentielles"
explorationString2 = "goûts musicaux pour la décennie:"
incontournableString = "Vos incontournables"

def getRecommendationsForDecade(startYear, endYear):
    
    # TODO - Get the recommendations from the helper functions
    return html.Div(id="viz4-container", className="column",children = [
        html.Div(id="viz4", children = [
            getVisualisation4Component(startYear, endYear),
        ]),
        html.Button('▼', id='generate-decade-button', className='generate-decade-button', value=f'{startYear-10}-{endYear-10}')    
])
    
def getVisualisation4Component(startYear, endYear):
    
    decadeString = str(endYear) + " - " + str(startYear)
    
    return html.Div(className="column", children = [
            html.Div(className="flex-container-space-between", children = [
                html.Div(className="title", children=[
                    html.H1([explorationString1, html.Br(), explorationString2], style={'margin-top': '15px'})
                ]),
                html.Div(className="column", children=[
                    html.Div(id="decade-text", children=decadeString),
                    html.Div(className="flex-container", children = [
                        html.Div(incontournableString, className="incontournable-text"),
                        html.Img(src='assets/star.png', className="star-icon")
                    ])
                ])
            ]),
            getDecadeContentComponents(tmpTopSongs, tmpTopArtists, tmpTopGenres),
        ])
    
def getDecadeContentComponents(songs, artists, genres):
    return html.Div(className="flex-container-space-between", children=[
        getTimelineComponent(songs, years, "Imagine", ["Details for song A", "Details for song B", "Details for song C", "Details for song D", "Details for song E", "Details for song F", "Details for song G", "Details for song H", "Details for song I", "Details for song J"]),
        html.Div(className="flex-container", style={'width': '50%'}, children=[
            getListOfRecommendationsComponents(artists, "artists", width='70%'),
            getListOfRecommendationsComponents(genres, "genres", width='70%') 
        ])
    ])

def getTimelineComponent(songs, years, star_song, song_details):
    timeline_items = []


    for song, year, details in zip(songs, years, song_details):
        timeline_item_content = [
            html.Div(year, className='timeline-year'),
            html.Div(song, className='timeline-song', title=details)
        ]

     
        if song == star_song:
            timeline_item_content.append(html.Img(src="assets/star.png", className="star-icon"))
        else:
            timeline_item_content.append(html.Div(className="transparent-star"))

        timeline_item = html.Div(timeline_item_content, className='timeline-item')
        timeline_items.append(timeline_item)


    timeline_container = html.Div(timeline_items, className='timeline-container')

    return timeline_container

    
def getListOfRecommendationsComponents(recommendations, id_suffix, width='50%'): 
    recommendations_components = []

    for i, recommendation in enumerate(recommendations):
        if i == 0: # TODO - Need to specify which recommendation is the star song
            recommendation_component = html.Span([
                recommendation,
                html.Img(src="assets/star.png", className="star-icon")
            ])
        else:
            recommendation_component = html.Span([
                recommendation,
                html.Div(className="transparent-star")
            ])

        recommendations_components.append(html.P(recommendation_component, className='recommendation'))

    return html.Div(
        id=f'recommendations-div-{id_suffix}',
        children=recommendations_components,
        className='recommendations-column',
        style={'width': width}
    )