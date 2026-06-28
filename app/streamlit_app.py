import streamlit as st
import pandas as pd
import os
from recommender import load_models, get_recommendation
from spotify_api import get_track_details

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
df = df.dropna(subset=['track_name', 'artists'])

df['first_artist'] = df['artists'].astype(str).str.split(';').str[0]

df['search_display'] = df['track_name'].astype(str) + " - " + df['first_artist']

features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

# main i-face
st.title("🎵 System Rekomendacji Muzyki")
st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit")

track_options = df['search_display'].unique().tolist()

search_query = st.selectbox(
    "Szukaj utworu:",
    options=track_options,
    index=None,
    placeholder="np, Numb - Linkin Park"
)
# search_query = st.text_input("Szukaj utworu:", placeholder="np. Numb")

# search logic
if search_query:
    with st.spinner("Przeszukuję bazę i analizuję wektory..."):
        results = get_recommendation(search_query, df, model, scaler, features)

        if results is not None:
            st.success("Znaleziono podobne utwory!")
            # st.dataframe(results)
            cols = st.columns(len(results))

            for col, (_, row) in zip(cols, results.iterrows()):
                with col:
                    cover_url, preview_url = get_track_details(row['track_id'])

                    if cover_url:
                        st.image(cover_url, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300?text=Brak+Okładki", use_container_width=True)

                    st.markdown(f"**{row['track_name']}**")
                    st.markdown(f"*{row['artists']}*")

                    st.link_button("Słuchaj w Spotify", f"https://open.spotify.com/track/{row['track_id']}")
        else:
            st.error("Nie znaleziono takiego utworu. Spróbuj wpisać inny tytuł")