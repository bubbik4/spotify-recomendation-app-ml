TODO: Spotify Music Recommender ML

[HIGH PRIORITY / NEXT SESSIONS]
- [x] Import 'get_track_details' from spotify_api.py into streamlit_app.py
- [x] Replace st.dataframe() with st.columns() to create a grid/tile layout
- [x] Fetch and display album covers for each recommended track
- [ ] Embed Spotify 30-second audio previews using st.audio() - ENDPOINT DEPRACATED

[MEDIUM PRIORITY / IMPROVEMENTS]
- [ ] Implement fallback placeholders (e.g., default image if API returns None for a cover)
- [ ] Add a visual spinner/loading state while fetching API data for all 5 recommendations
- [ ] Add interactive sliders on the sidebar to adjust algorithm weights (e.g., preference for "energy" or "acousticness")
- [ ] Add filtered search for improved search UX
- [ ] Add DNS record and Nginx forward for spotify-ml subdomain 

[LOW PRIORITY / BACKLOG]
- [ ] Extract feature lists and configuration variables into a separate config.py file
- [ ] Add more robust error handling for edge cases (e.g., API timeouts)
- [ ] Prepare the application for deployment (e.g., Streamlit Community Cloud)