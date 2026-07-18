# app/config.py

# Lista cech używanych do obliczania dystansu przy rekomendacjach
FEATURES = [
    'danceability', 
    'energy', 
    'speechiness', 
    'acousticness', 
    'instrumentalness', 
    'liveness', 
    'valence', 
    'tempo'
]

# Domyślna liczba rekomendacji do wyświetlenia
NUM_RECOMMENDATIONS = 5
