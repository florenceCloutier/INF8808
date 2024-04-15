import dash_html_components as html

methodology_text = """
Après avoir lu et préparé les données, les attributs numériques ont été normalisés 
à l'aide de la mise à l'échelle Min-Max. Les valeurs moyennes de ces attributs ont été 
calculées pour chaque genre musical et chaque artiste. De plus, une carte associant les
genres principaux à leurs sous-genres respectifs a été créée. Le profil de l'utilisateur 
correspond ainsi à une moyenne de tous les attributs des chansons contenues dans les sélections d'artistes. 
Pour profiler les préférences des utilisateurs, une distance euclidienne a été utilisée 
entre les moyennes des attributs et le profil de l'utilisateur. Dans le cas d'une chanson individuelle, 
la distance entre les attributs de cette chanson et le profil de l'usager a également été calculée.
Le jeu de données utilisé est disponible à l'adresse suivante :https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs
"""

def getMethodologyComponent():
    return html.Div(
        className='methodology-container',
        children=[
            methodology_text
        ]
    )
    
