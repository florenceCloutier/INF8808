import dash_html_components as html
import dash_table
import dash_core_components as dcc
import plotly.graph_objects as go

tmpTopSongs = ["Chanson A", "Chanson B", "Chanson C", "Chanson D", "Chanson E", "Chanson F", "Chanson G", "Chanson H", "Chanson I", "Chanson J",
               "Chanson K", "Chanson L", "Chanson M", "Chanson N", "Chanson O", "Chanson P", "Chanson Q", "Chanson R", "Chanson S", "Chanson T",
               "Chanson U", "Chanson V", "Chanson W", "Chanson X", "Chanson Y", "Chanson Z", "Chanson AA", "Chanson AB", "Chanson AC", "Chanson AD",
               "Chanson AE", "Chanson AF", "Chanson AG", "Chanson AH", "Chanson AI", "Chanson AJ", "Chanson AK", "Chanson AL", "Chanson AM", "Chanson AN",
               "Chanson AO", "Chanson AP", "Chanson AQ", "Chanson AR", "Chanson AS", "Chanson AT", "Chanson AU", "Chanson AV", "Chanson AW", "Chanson AX"]

tmpTopArtists = ["Artiste A", "Artiste B", "Artiste C", "Artiste D", "Artiste E", "Artiste F"]
tmpTopGenres = ["Genre A", "Genre B", "Genre C", "Genre D", "Genre E"]

years = [2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010,
         2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000,
         1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990,
         1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980,
         1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970,]

explorationString = "Exploration de vos potentielles goûts musicaux pour la décennie"
incontournableString = "Vos incontournables"

def getRecommendationsForDecade(startYear, endYear):
    
    # TODO - Get the recommendations from the helper functions
    
    return html.Div(className="testing", children = [
        getHeaderOfDecadeComponent(startYear, endYear),
    ])
    
def getHeaderOfDecadeComponent(startYear, endYear):
    
    decadeString = str(startYear) + " - " + str(endYear)
    
    return html.Div(className="column", children = [
            html.Div(className="flex-container-space-between", children = [
                html.H1(explorationString),
                html.Div(className="column", children=[
                    html.Div(id="decade-text", children=decadeString),
                    html.Div(className="flex-container", children = [
                        html.Div(incontournableString),
                        html.Img(src='assets/star.png', className="star-icon")
                    ])
                ])
            ]),
            getDecadeContentComponents(tmpTopSongs, tmpTopArtists, tmpTopGenres),
        ])
    
def getDecadeContentComponents(songs, artists, genres):
    return html.Div(className="flex-container-space-between", children=[
        getTimelineComponent(songs, years),
        html.Div(className="flex-container", style={'width': '50%'}, children=[
            getListOfRecommendationsComponents(artists, "artists", width='70%'),  # Adjust width here
            getListOfRecommendationsComponents(genres, "genres", width='70%')  # Adjust width here
        ])
    ])

def getTimelineComponent(songs, years):
    timeline_items = []

    # Create a vertical timeline item for each year and its associated song
    for song, year in zip(songs, years):
        timeline_item = html.Div([
            html.Div(year, className='timeline-year'),
            html.Div(song, className='timeline-song')
        ], className='timeline-item')
        timeline_items.append(timeline_item)

    # Wrap all timeline items in a container
    timeline_container = html.Div(timeline_items, className='timeline-container')

    return timeline_container

    
def getListOfRecommendationsComponents(recommendations, id_suffix, width='50%'):  # Add width parameter
    # Add the star image to the first recommendation
    recommendations[0] = html.Span([
        recommendations[0],
        html.Img(src="assets/star.png", className="star-icon")
    ])

    return html.Div(
        id=f'recommendations-div-{id_suffix}',
        children=[html.P(recommendation, className='recommendation') for recommendation in recommendations],
        className='recommendations-column',
        style={'width': width}  # Set width style here
    )