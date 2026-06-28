# TODO: Spotify Music Recommender ML

### [HIGH PRIORITY / NEXT SESSIONS]
- [x] ~~Import 'get_track_details' from spotify_api.py into streamlit_app.py~~
- [x] ~~Replace st.dataframe() with st.columns() to create a grid/tile layout~~
- [x] ~~Fetch and display album covers for each recommended track~~
- [x] ~~Implement fallback placeholders (e.g., default image if API returns None for a cover)~~
- [x] ~~Add a visual spinner/loading state while fetching API data for all 5 recommendations~~
- [x] ~~Fix search logic to handle long artist names and exact matching (Data Cleaning)~~
- [ ] **Optimize performance:** Move DataFrame preprocessing (`first_artist` and `search_display` columns) inside `@st.cache_data` to prevent CPU overhead on every click.
- [ ] **Fix UI lag:** Implement 2-stage search (Text Input for >=3 chars -> Selectbox) to reduce browser payload.

### [MEDIUM PRIORITY / IMPROVEMENTS]
- [ ] Add interactive sliders on the sidebar to adjust algorithm weights (e.g., preference for "energy" or "acousticness")
- [ ] Add DNS record and Nginx forward for spotify-ml subdomain 
- [ ] Embed Spotify 30-second audio previews using st.audio() - *NOTE: ENDPOINT DEPRECATED (Consider dropping or finding a workaround)*

### [LOW PRIORITY / BACKLOG]
- [ ] Extract feature lists and configuration variables into a separate config.py file
- [ ] Add more robust error handling for edge cases (e.g., API timeouts, network errors)
- [ ] Prepare the application for deployment (e.g., Streamlit Community Cloud / Docker)