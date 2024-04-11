#%%
import pandas as pd
import numpy as np
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
        self.df_initial_data = pd.read_csv('./data/spotify_songs.csv')
        self.criterias = [
            'danceability', 'energy', 'loudness', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 
            'valence', 'tempo', 'duration_ms'
        ]
        self.descriptions = [
            'Niveau auquel une chanson est compatible avec la danse',
            'Mesure de l’intensité et de l’activité',
            'Mesure de l’intensité sonore',
            'Mesure le niveau de parole dans une musique',
            'Mesure le niveau d’acoustique dans une chanson',
            'Mesure l’absence de niveau de parole dans une musique',
            'Mesure s’il y avait une audience lors de l’enregistrement',
            'Mesure si une chanson est joyeuse ou triste',
            'Mesure du tempo de la chanson',
            'Durée de la chanson en millisecondes'
        ]
        self.decade_genre_cache = pd.DataFrame()
        self.artist_decade_cache = pd.DataFrame()
        self.songs_decade_cache = pd.DataFrame()
        
        self.genres_list = self.df_data['playlist_genre'].unique().tolist()
        self.attributes_by_genre = self.compute_attributes_by_genre()
        
        
        self.artists_list = self.df_data['track_artist'].unique().tolist()
        self.attributes_by_artist = self.compute_attributes_by_artist()
    
    def compute_attributes_by_genre(self):
        """
        attributes_by_genre = pd.DataFrame(columns=self.criterias)
        for genre in self.genres_list:
            genre_data = self.df_data[self.df_data['playlist_genre'] == genre]
            genre_mean = genre_data[self.criterias].mean()
            attributes_by_genre.loc[genre] = genre_mean
        
        attributes_by_genre.to_csv('genre')
        """
        return pd.read_csv("../data/attributes_by_genre.csv", index_col = False)
    
    def compute_attributes_by_artist(self):
        """
        attributes_by_artist = pd.DataFrame(columns=self.criterias)
        for artist in self.artists_list:
            artist_data = self.df_data[self.df_data['track_artist'] == artist]
            artist_mean = artist_data[self.criterias].mean()
            attributes_by_artist.loc[artist] = artist_mean
        attributes_by_artist.to_csv('artist')
        print(attributes_by_artist.head())
        """
        return pd.read_csv("../data/attributes_by_artist.csv", index_col = False)    
            
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
    
    ## ------  Profil  -----------
    def generate_genres_list(self):
        return self.genres_list
    
    def generate_artists_list(self):
        artists_list = self.df_data['track_artist'].unique().tolist()
        return artists_list
    
    def generate_sample_artists_from_genres(self, selected_genres):
        attributes = pd.DataFrame(columns=self.criterias)
        distances_df = pd.DataFrame(columns=['distance'])
        
        attributes = self.attributes_by_genre[self.attributes_by_genre.iloc[:, 0].isin(selected_genres)]
        total_attributes = attributes[self.criterias].mean()
        distances_df['distance'] = np.linalg.norm(self.attributes_by_artist.iloc[:, 1:].values - total_attributes.values, axis=1)
        
        artist_names = self.attributes_by_artist.iloc[distances_df['distance'].nsmallest(6).index]['Unnamed: 0'].tolist()
        print(artist_names)

        return artist_names
    
    def generate_profil_attributes(self, selected_artist, selected_genre):
        dict_pref = {'artistes':selected_artist,
                     'sous_genres':selected_genre}
        
        return dict_pref
    
    ## ------  Visualisation 1  -----------

    def generate_user_preferences_dict(self,dict_pref):
        criterias = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']
        pref_values = {}
        df_filtered = self.df_data[self.df_data['track_artist'].isin(dict_pref['artistes']) & self.df_data['playlist_subgenre'].isin(dict_pref['sous_genres'])]
        for criteria in criterias:            
            pref_values[criteria] = df_filtered[criteria].mean()
        return pref_values
    
    def generate_real_user_preferences_dict(self,dict_pref):
        df = self.df_initial_data
        real_pref_values = {}
        df_filtered = df[df['track_artist'].isin(dict_pref['artistes']) & df['playlist_subgenre'].isin(dict_pref['sous_genres'])]
        for criteria in self.criterias:
            real_pref_values[criteria] = df_filtered[criteria].mean()
        return real_pref_values
        


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
        print(user_pref_dict)
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
        return df_compare.reset_index(), mean_pref_values
    
    def get_initial_values_by_type(self,name,type):
        if type == 'chansons':
            df = self.df_initial_data.groupby(['track_artist','track_name','track_popularity'])[self.criterias].mean().reset_index()
            return df[df['track_name'] == name]
        elif type == 'artistes':
            real_pref_values = {}
            df = self.df_initial_data.groupby(['track_artist'])[self.criterias].mean().reset_index()
            df_filtered = df[df['track_artist'] == name]
            for criteria in self.criterias:
               real_pref_values[criteria] = df_filtered[criteria].mean()
            real_pref_df = pd.DataFrame.from_dict(real_pref_values,orient='index').T
            return real_pref_df
        elif type == 'playlist':
            real_pref_values = {}
            df = self.df_initial_data.groupby(['playlist_name'])[self.criterias].mean().reset_index()
            df_filtered = df[df['playlist_name'] == name]
            for criteria in self.criterias:
               real_pref_values[criteria] = df_filtered[criteria].mean()
            real_pref_df = pd.DataFrame.from_dict(real_pref_values,orient='index').T
            return real_pref_df

## ------  Visualisation 4  -----------
    
    def generate_yearly_song_recommendation(self,dict_pref):
        """Fonction pour générer un dataframe avec les chansons les plus similaires au profil, 
        par année, sous forme de dataframe avec les caractéristiques.

        Args:
            dict_pref (Dict): Un dictionnaire avec les préférences utilisateurs

        Returns:
            DataFrame: Dataframe avec les chansons par année qui sont les plus proches du profil
        """
        if self.songs_decade_cache.empty == False:
            return self.songs_decade_cache
        
        criterias = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']

        self.df_data['year'] = pd.to_datetime(self.df_data['track_album_release_date'], format='%Y-%m-%d').dt.year
        df_compare = self.df_data.groupby(['track_name','track_album_name','year','track_artist','track_popularity'])[criterias].mean()

        user_pref_dict = self.generate_user_preferences_dict(dict_pref)
        user_pref_df = pd.DataFrame([user_pref_dict], columns=user_pref_dict.keys())
        df_compare['similarity'] = df_compare[criterias].apply(lambda x: 1 - distance.euclidean(x, user_pref_df.values.flatten()), axis=1)
        df_compare = df_compare.reset_index()

        max_similarity_per_year = df_compare.groupby('year')['similarity'].max().reset_index()
        df_max_similarity = pd.merge(df_compare, max_similarity_per_year, on=['year', 'similarity'])
        df_max_similarity = df_max_similarity.drop_duplicates(subset=['year', 'similarity'])
        song_similarity = df_max_similarity.reset_index(drop=True)
        
        self.songs_decade_cache = song_similarity
        return song_similarity
    
    def generate_yearly_artist_recommendation(self,dict_pref):
        """Fonction pour générer un dataframe avec les artiste les plus similaires au profil, 
        par année, sous forme de dataframe avec les caractéristiques.

        Args:
            dict_pref (Dict): Un dictionnaire avec les préférences utilisateurs

        Returns:
            DataFrame: Dataframe avec les artistes par année qui sont les plus proches du profil
        """
        if self.artist_decade_cache.empty == False:
            return self.artist_decade_cache
        
        criterias = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']

        self.df_data['year'] = pd.to_datetime(self.df_data['track_album_release_date'], format='%Y-%m-%d').dt.year
        df_compare = self.df_data.groupby(['year','track_artist'])[criterias].mean()

        user_pref_dict = self.generate_user_preferences_dict(dict_pref)
        user_pref_df = pd.DataFrame([user_pref_dict], columns=user_pref_dict.keys())
        df_compare['similarity'] = df_compare[criterias].apply(lambda x: 1 - distance.euclidean(x, user_pref_df.values.flatten()), axis=1)
        df_compare = df_compare.reset_index()

        max_similarity_per_year = df_compare.groupby('year')['similarity'].max().reset_index()
        df_max_similarity = pd.merge(df_compare, max_similarity_per_year, on=['year', 'similarity'])
        df_max_similarity = df_max_similarity.drop_duplicates(subset=['year', 'similarity'])
        artist_similarity = df_max_similarity.reset_index(drop=True)
        
        self.artist_cache = artist_similarity
        return artist_similarity
    
    def generate_yearly_genre_recommendation(self,dict_pref):
        """Fonction pour générer un dataframe avec les genres les plus similaires au profil, 
        par année, sous forme de dataframe avec les caractéristiques.

        Args:
            dict_pref (Dict): Un dictionnaire avec les préférences utilisateurs

        Returns:
            DataFrame: Dataframe avec les genres par année qui sont les plus proches du profil
        """
        if self.decade_genre_cache.empty == False:
            return self.decade_genre_cache
        
        criterias = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']

        self.df_data['year'] = pd.to_datetime(self.df_data['track_album_release_date'], format='%Y-%m-%d').dt.year
        df_compare = self.df_data.groupby(['year','playlist_genre'])[criterias].mean()

        user_pref_dict = self.generate_user_preferences_dict(dict_pref)
        user_pref_df = pd.DataFrame([user_pref_dict], columns=user_pref_dict.keys())
        df_compare['similarity'] = df_compare[criterias].apply(lambda x: 1 - distance.euclidean(x, user_pref_df.values.flatten()), axis=1)
        df_compare = df_compare.reset_index()

        max_similarity_per_year = df_compare.groupby('year')['similarity'].max().reset_index()
        df_max_similarity = pd.merge(df_compare, max_similarity_per_year, on=['year', 'similarity'])
        df_max_similarity = df_max_similarity.drop_duplicates(subset=['year', 'similarity'])
        genre_similarity = df_max_similarity.reset_index(drop=True)
        
        self.decade_genre_cache = genre_similarity
        return genre_similarity
        
        

    

# %%
