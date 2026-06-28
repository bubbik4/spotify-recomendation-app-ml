import joblib
import os

def load_models():
    # Dynamic path building to `data` directory
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, '..', 'data')

    # Importing Colab artifacts
    model = joblib.load(os.path.join(data_dir, 'model.pkl'))
    scaler = joblib.load(os.path.join(data_dir, 'scaler.pkl'))

    return model, scaler

def get_recommendation(search_query, df, model, scaler, features):
    # Searching by song name
    # matched_songs = df[df['search_display'].str.contains(search_query, case=False, na=False, regex=False)]
    matched_songs = df[df['search_display'] == search_query]

    if matched_songs.empty:
        return None
    
    
    song_data = matched_songs.iloc[0]
    song_features = song_data[features].values.reshape(1, -1)
    song_scaled = scaler.transform(song_features)

    distances, indices = model.kneighbors(song_scaled)

    # Results to a table
    recommended_df = df.iloc[indices[0]].copy()
    recommended_df['cosine_distance'] = distances[0]

    return recommended_df[['master_id', 'track_id', 'track_name', 'artists', 'cosine_distance']]