import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash import callback_context

import helpers

path_name = './data/spotify_songs.csv'
helper = helpers.Helper(path_name)
sub_genres_list = helper.sub_genres

# Function to generate recommendations based on selected genres
# Create a grid of buttons
def create_button_grid():
    buttons = []
    for genre in sub_genres_list:
        buttons.append(html.Button(genre, id={'type': 'button', 'index': genre}))
    button_grid = html.Div([html.Div(buttons[i:i+4], className='row') for i in range(0, len(buttons), 4)])
    return button_grid

# Callback to update selected genres list
def update_selected_genres_callback(app):
    @app.callback(
        Output('selected-genres-output', 'children'),
        [Input({'type': 'button', 'index': 'all'}, 'n_clicks')],
        [State({'type': 'button', 'index': 'all'}, 'n_clicks_timestamp')],
    )
    def update_selected_genres(n_clicks, n_clicks_timestamp):
        selected_genres = []
        ctx = callback_context
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            for genre, timestamp in zip(sub_genres_list, n_clicks_timestamp):
                if n_clicks[genre] and n_clicks[genre] % 2 != 0:  # Toggle logic
                    selected_genres.append(genre)
                    print(selected_genres)
        return html.Div([
            html.Span(genre, className='selected-genre') for genre in selected_genres
        ])
    return update_selected_genres

# Callback to reset selected genres list when submit button is clicked
def reset_selected_genres_callback(app):
    @app.callback(
        Output('selected-genres-output', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State({'type': 'button', 'index': 'all'}, 'n_clicks_timestamp')]
    )
    def reset_selected_genres(n_clicks, n_clicks_timestamp):
        if n_clicks:
            selected_genres = [genre for genre, timestamp in zip(sub_genres_list, n_clicks_timestamp)
                               if timestamp and timestamp % 2 != 0]
            print("Submitted genres:", selected_genres)
            return ''
        else:
            raise dash.exceptions.PreventUpdate
    return reset_selected_genres_callback