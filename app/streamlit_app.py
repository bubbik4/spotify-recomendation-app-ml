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
    data_path = os.path.join(current_dir, '..', 'data', 'tracks_features.csv')
    df = pd.read_csv(data_path)
    
    df = df.rename(columns={'name': 'track_name', 'id': "track_id"})

    df = df.dropna(subset=['track_name', 'artists'])
    df['first_artist'] = df['artists'].astype(str).str.split(';').str[0]
    df['search_display'] = df['track_name'].astype(str) + " - " + df['first_artist']
    
    return df
    
# backend init
model, scaler = get_ml_components()
df = load_data()
features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

# main i-face
st.title("🎵 System Rekomendacji Muzyki")
st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit")

# search_query = st.selectbox(
#     "Szukaj utworu:",
#     options=track_options,
#     index=None,
#     placeholder="np. Numb - Linkin Park"
# )
# search_query = st.text_input("Szukaj utworu:", placeholder="np. Numb")

# search logic
col1, col2 = st.columns(2)

with col1:
    search_text = st.text_input("1. Wpisz tytuł:", placeholder="np. Numb")

if search_text and len(search_text) >= 3:
    filtered_df = df[df['search_display'].str.contains(search_text, case=False, na=False)]

    if not filtered_df.empty:
        track_options = filtered_df['search_display'].unique().tolist()
        
        with col2:
            search_query = st.selectbox(
                "2. Doprecyzuj wykonanie:",
                options=track_options,
                index=None
            )

        # WCIĘCIE: Cała logika odpalania modelu musi być TUTAJ, wewnątrz warunku
        if search_query:
            with st.spinner("Przeszukuję bazę i analizuję wektory..."):
                results = get_recommendation(search_query, df, model, scaler, features)

                if results is not None:
                    st.success("Znaleziono podobne utwory!")
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
    else:
        st.info("Nie znaleziono utworów pasujących do wpisanej frazy")