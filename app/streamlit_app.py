import streamlit as st
import pandas as pd
import os

# Konfiguracja głównego okna aplikacji
st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="wide")

st.title("🎵 System Rekomendacji Muzyki")
st.write("Witaj! Jeśli widzisz ten tekst, Twój lokalny serwer Streamlit działa poprawnie.")

# Bezpieczne budowanie ścieżki niezależnie od systemu operacyjnego
# Zakładamy, że jesteśmy w 'app/streamlit_app.py', więc musimy cofnąć się o poziom wyżej
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, '..', 'data', 'spotify_cleaned.csv')

# Test podłączenia warstwy danych
try:
    df = pd.read_csv(data_path)
    st.success(f"Warstwa analityczna podpięta pomyślnie! Liczba utworów w bazie: {len(df)}")
    # Interaktywna tabela na frontendzie (będziesz mógł ją sortować i przeszukiwać w przeglądarce)
    st.dataframe(df.head(5))
except FileNotFoundError:
    st.error(f"Nie znaleziono pliku z danymi. Oczekiwana ścieżka: {data_path}")