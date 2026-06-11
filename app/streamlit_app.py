import streamlit as st
import pandas as pd
import os
from recommender import load_models, get_recommendation

# Konfiguracja głównego okna aplikacji
st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="wide")

# Model ML to cache, so it would olny load on server startup
@st.cache_resource
def get_ml_components():
    return load_models()

# CSV to RAM
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, '..', 'data', 'spotify_cleaned.csv')
    return pd.read_csv(data_path)
    
# backend init
model, scaler = get_ml_components()
df = load_data()
features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

# main i-face
st.title("🎵 System Rekomendacji Muzyki")
st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit")

search_query = st.text_input("Szukaj utworu:", placeholder="np. Numb")

# search logic
if search_query:
    with st.spinner("Przeszukuję bazę i analizuję wektory..."):
        results = get_recommendation(search_query, df, model, scaler, features)

        if results is not None:
            st.success("Znaleziono podobne utwory!")
            st.dataframe(results)
        else:
            st.error("Nie znaleziono takiego utworu. Spróbuj wpisać inny tytuł")