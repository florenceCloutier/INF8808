import dash_html_components as html

methodology_text = """
Méthodologie: Après avoir lu et préparé les données, les attributs numériques 
ont été normalisé à l'aide de la mise à l'échelle Min-Max, les valeurs moyennes des 
attributs ont été calculé pour chaque genre musical et chaque artiste, 
ainsi que créé une carte associant les genres principaux à leurs sous-genres respectifs.
Le profil de l'utilisateur correspond donc a une moyenne de tous les attributs des chansons
contenu dans les artistes sélectionnés. Pour profiler les préférences des utilisateurs,
une distance euclédienne a été utilisé entre les moyennes des attributs et le profil.
Dans le cas d'une chanson individuelle la distance entre les attributs d'une chanson
et le profil usager a été utilisé. Le jeux de données utilisés est disponible à 
l'addresse suivante: https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs
"""

def getMethodologyComponent():
    return html.Div(
        className='methodology-container',
        children=[
            methodology_text
        ]
    )
    
