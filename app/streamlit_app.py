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
    df = pd.read_csv(data_path)
    
    df = df.rename(columns={'name': 'track_name', 'id': "track_id"})

    df = df.dropna(subset=['track_name', 'artists'])
    df['first_artist'] = df['artists'].astype(str).str.replace(r"\[|\]|'|\"", "", regex=True).str.split(',').str[0].str.strip()
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
            song_data = df[df['search_display'] == search_query].iloc[0]
            
            st.sidebar.header("Kalibracja modelu")
            st.sidebar.write("Dostosuj wagi, aby wymusić kierunek rekomendacji")
            with st.sidebar.form(key="weights_form"):
                custom_features = []
                for feature in features:
                    min_val = float(df[feature].min())
                    max_val = float(df[feature].max())
                    actual_val = float(song_data[feature])
                    
                    actual_val = max(min_val, min(max_val, actual_val))
                    
                    val = st.slider(
                        f"{feature}",
                        min_value=min_val,
                        max_value=max_val,
                        value=actual_val,
                        step=1.0 if feature == 'tempo' else 0.01
                    )
                    custom_features.append(val)
                submit_button = st.form_submit_button(label="Zastosuj")

            with st.spinner("Przeszukuję bazę i analizuję wektory..."):
                results = get_recommendation(search_query, df, model, scaler, features, custom_features=custom_features)

                if results is not None:
                    st.success("Znaleziono podobne utwory!")
                    cols = st.columns(len(results))

                    for col, (_, row) in zip(cols, results.iterrows()):
                        with col:
                            cover_url, preview_url = get_track_details(row['track_id'])

                            # NAPRAWIONE WCIĘCIA:
                            if cover_url:
                                st.image(cover_url, use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/300?text=Brak+Okładki", use_container_width=True)

                            # truncate = lambda text: str(text) if len(str(text)) <= 35 else str(text)[:32] + "..."
                            # st.markdown(f"**{truncate(row['track_name'])}**")
                            # st.markdown(f"*{truncate(row['artists'])}*")
                            
                            title_html = f'<div style="height: 3.5rem; overflow: hidden; margin-bottom: 0.5rem; line-height: 1.2;"><b>{row["track_name"]}</b></div>'
                            artist_html = f'<div style="height: 2.5rem; overflow: hidden; line-height: 1.2;"><i>{row["artists"]}</i></div>'
                            
                            st.markdown(title_html, unsafe_allow_html=True)
                            st.markdown(artist_html, unsafe_allow_html=True)

                            st.link_button("Słuchaj w Spotify", f"https://open.spotify.com/track/{row['track_id']}")                            
                            with st.expander("Zobacz parametry"):
                                for f in features:
                                    st.caption(f"**{f.capitalize()}**: {row[f]:.2f}")
                else:
                    st.error("Nie znaleziono takiego utworu. Spróbuj wpisać inny tytuł")
    else:
        st.info("Nie znaleziono utworów pasujących do wpisanej frazy")