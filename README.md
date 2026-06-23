Spotify Music Recommender to interaktywna aplikacja webowa oparta na uczeniu maszynowym, stworzona do odkrywania nowej muzyki. Zamiast opierać się na popularności czy gatunkach, silnik aplikacji wykorzystuje algorytm K-Najbliższych Sąsiadów (K-NN) do analizy fizycznych cech dźwiękowych utworów – takich jak energia, taneczność (danceability), akustyczność czy tempo. Wpisując swój ulubiony utwór, użytkownik otrzymuje spersonalizowaną listę rekomendacji o zbliżonym profilu brzmieniowym. Całość jest zintegrowana z oficjalnym API Spotify, co pozwala na płynne wyświetlanie okładek albumów oraz odsłuchiwanie 30-sekundowych próbek audio bezpośrednio w przeglądarce.

Główne funkcjonalności:

    Silnik ML: Wyszukiwanie podobnych utworów za pomocą modelu K-NN (scikit-learn) wytrenowanego na obszernym zbiorze danych Spotify.

    Integracja API: Dynamiczne pobieranie metadanych (okładki, linki preview) w czasie rzeczywistym przy użyciu biblioteki Spotipy.

    Interfejs użytkownika: Nowoczesny, responsywny widok zbudowany w frameworku Streamlit, renderujący wyniki w formie czytelnych kafelków.

Stos technologiczny:
Python, Streamlit, scikit-learn, pandas, Spotipy (Spotify API OAuth2).