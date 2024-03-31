#%%
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial import distance

""" 
    Exemple: dict_pref = {
    'sous_genres' : ['trap','neo soul','tropical'],
    'artistes': ['Ed Sheeran','Metallica','Drake']
}

    path_name = './data/spotify_songs.csv'

    df_data = read_data(path_name)
    
    Exemple d'utilisation:
        user_pref_dict = help.generate_user_preferences_dict(user_preferences)
        print("User Preferences Dictionary:")
        print(user_pref_dict)

        # Generate a dictionary with average preferences across all data
        average_pref_dict = help.generate_average_preferences_dict()
        print("\nAverage Preferences Dictionary:")
        print(average_pref_dict)

        # Generate a DataFrame showing similarity between user preferences and subgenres
        subgenre_similarity_df = help.generate_subgenre_similarity_df(user_preferences)
        print("\nSubgenre Similarity DataFrame:")
        print(subgenre_similarity_df.head())  # Show the first few rows

        # Generate recommendations (e.g., songs) based on user preferences
        recommendations_df, mean_pref_values = help.generate_recommendations_df(user_preferences, recommendation_type='chansons')
        print("\nRecommendations DataFrame:")
        print(recommendations_df.head())  # Show the first few rows
        print("\nMean Preferences Values for Recommendations:")
        print(mean_pref_values)


"""

class Helper:
    def __init__(self,path):
        self.df_data = self.read_data(path)
        self.criterias = [
            'danceability', 'energy', 'loudness', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 
            'valence', 'tempo', 'duration_ms'
        ]
        self.sub_genres = self.df_data['playlist_subgenre'].unique()
        
    def read_data(self, path):
        df = pd.read_csv(path)
        numerical_columns = df.select_dtypes(include=['float64', 'int64'])
        #Normalisation par la moyenne
        for column in numerical_columns:
            col_mean = df[column].mean()
            col_range = df[column].max() - df[column].min()
            if col_range != 0:  # To avoid division by zero
                df[column] = (df[column] - col_mean) / col_range

        # scaler = MinMaxScaler()
        # normalized_data = scaler.fit_transform(numerical_columns)
        # df_normalized = pd.DataFrame(normalized_data, columns=numerical_columns.columns, index=df.index)
        # df.update(df_normalized)
        return df

 
    ## ------  Visualisation 1  -----------

    def generate_user_preferences_dict(self,dict_pref):
        criterias = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']
        pref_values = {}
        df_filtered = self.df_data[self.df_data['track_artist'].isin(dict_pref['artistes']) & self.df_data['playlist_subgenre'].isin(dict_pref['sous_genres'])]
        for criteria in criterias:            
            pref_values[criteria] = df_filtered[criteria].mean()
        return pref_values


    def generate_average_preferences_dict(self):
        criterias = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']
        mean_pref_values = {}
        for criteria in criterias:            
            mean_pref_values[criteria] = self.df_data[criteria].mean()
        return mean_pref_values

    ## ------  Visualisation 2  -----------

    def generate_subgenre_similarity_df(self,dict_pref):
        criterias = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']
        df_subgenres = self.df_data.groupby(['playlist_genre','playlist_subgenre'])[criterias].mean().reset_index()
        user_pref_dict = self.generate_user_preferences_dict(dict_pref)
        user_pref_df = pd.DataFrame([user_pref_dict], columns=user_pref_dict.keys())
        df_subgenres['similarity'] = df_subgenres[criterias].apply(lambda x: 1 - distance.euclidean(x, user_pref_df.values.flatten()), axis=1)
        return df_subgenres[['playlist_genre','playlist_subgenre','similarity']]

    ## ------  Visualisation 3  -----------

    def generate_recommendations_df(self,dict_pref, recommendation_type='chansons'):
        """Fonction pour générer un dataframe avec les recommendations selon le type, 
        en plus du dictionnaire nécessaire pour le radar chart.

        Args:
            dict_pref (Dict): Un dictionnaire avec les préférences utilisateurs
            recommendation_type (str, optional): Choix du type de recommendations ('chansons','artistes' ou 'playlist'). 
                Defaults to 'chansons'.

        Returns:
            DataFrame: Dataframe avec la comparaison des chansons/artistes/playlist avec le score de similarité (0->1)
            Dict: dictionnaire qui contient les valeurs moyennes de la sélection
        """
        criterias = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']
        if recommendation_type == 'chansons':
            df_compare = self.df_data.groupby(['track_artist','track_name','track_popularity'])[criterias].mean()
        elif recommendation_type == 'artistes':
            df_compare = self.df_data.groupby(['track_artist'])[criterias].mean()
        elif recommendation_type == 'playlist':
            df_compare = self.df_data.groupby(['playlist_name'])[criterias].mean()
        user_pref_dict = self.generate_user_preferences_dict(dict_pref)
        user_pref_df = pd.DataFrame([user_pref_dict], columns=user_pref_dict.keys())
        df_compare['similarity'] = df_compare[criterias].apply(lambda x: 1 - distance.euclidean(x, user_pref_df.values.flatten()), axis=1)
        df_compare = df_compare.sort_values(by='similarity',ascending=False).head(10)
        mean_pref_values = {}
        for criteria in criterias:            
            mean_pref_values[criteria] = df_compare[criteria].mean()
        return df_compare, mean_pref_values

# %%
