import joblib
import os
import numpy as np

def load_models():
    # Dynamic path building to `data` directory
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, '..', 'data')

    # Importing Colab artifacts
    # model = joblib.load(os.path.join(data_dir, 'model.pkl'))
    # scaler = joblib.load(os.path.join(data_dir, 'scaler.pkl'))
    model = joblib.load(os.path.join(data_dir, 'model.pkl'))
    scaler = joblib.load(os.path.join(data_dir, 'scaler.pkl'))

    return model, scaler

def get_recommendation(search_query, df, model, scaler, features, custom_features=None):
    matched_songs = df[df['search_display'] == search_query]

    if matched_songs.empty:
        return None
    
    if custom_features is not None:
        song_features = np.array(custom_features).reshape(1, -1)
    else:
        song_data = matched_songs.iloc[0]
        song_features = song_data[features].values.reshape(1, -1)

    song_scaled = scaler.transform(song_features)
    distances, indices = model.kneighbors(song_scaled)

    recommended_df = df.iloc[indices[0]].copy()
    recommended_df['cosine_distance'] = distances[0]

    columns_to_return = ['track_id', 'track_name', 'artists', 'cosine_distance'] + features
    return columns_to_return

    # if weights:
    #     # Tworzymy wektor wag w takiej samej kolejności co features
    #     # weight_vector = [weights[f] for f in features]
    #     # Wymnażamy wartości wektora startowego
    #     # song_scaled = song_scaled * weight_vector

    # distances, indices = model.kneighbors(song_scaled)

    # recommended_df = df.iloc[indices[0]].copy()
    # recommended_df['cosine_distance'] = distances[0]