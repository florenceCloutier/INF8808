import dash_html_components as html
import dash_table

tmpTopSongs = ["Chanson A", "Chanson B", "Chanson C", "Chanson D", "Chanson E", "Chanson F", "Chanson G", "Chanson H", "Chanson I", "Chanson J"]
tmpTopArtists = ["Artiste A", "Artiste B", "Artiste C", "Artiste D", "Artiste E", "Artiste F"]
tmpTopGenres = ["Genre A", "Genre B", "Genre C", "Genre D", "Genre E"]

years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

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
            getDecadeContentComponent(tmpTopSongs, tmpTopArtists, tmpTopGenres),
        ])
    
def getDecadeContentComponent(songs, artists , genres):
    return html.Div(className="flex-container-space-between", children = [
        getSongsComponent(songs, years),
        html.Div(className="flex-container", children = [
            getListOfRecommendationsComponents(artists, "artists"),
            getListOfRecommendationsComponents(genres, "genres")
        ])
    ])

def getSongsComponent(songs, years):
    # Add the star image to the first song
    songs[0] = f'{songs[0]} <img src="assets/star.png" class="star-icon"/>'

    return dash_table.DataTable(
        id='table',
        columns=[
            {"name": "Year", "id": "Year"},
            {"name": "Songs", "id": "Songs", 'presentation': 'markdown'}
        ],
        data=[{"Year": year, "Songs": song} for year, song in zip(years, songs)],
        active_cell=None,  # Disable active cell selection,
        cell_selectable=False,  # Disable cell selection
        style_cell={'textAlign': 'left', 'border': 'none'},  # Remove cell borders
        style_header={'display': 'none'},  # Hide header
        style_data={'border-bottom': '1px solid #d6d6d6', 'user-select': 'none'},  # Add bottom border to data cells
        style_cell_conditional=[
            {'if': {'column_id': 'Songs'}, 'width': '50%'},  # Set width of Songs column
        ],
        markdown_options={'html': True}  # Allow HTML in cells
    )
    
def getListOfRecommendationsComponents(recommendations, id_suffix):
    # Add the star image to the first recommendation
    recommendations[0] = html.Span([
        recommendations[0], 
        html.Img(src="assets/star.png", className="star-icon")
    ])

    return html.Div(
        id=f'recommendations-div-{id_suffix}',
        children=[html.P(recommendation, className='recommendation') for recommendation in recommendations],
        className='recommendations-column'
    )