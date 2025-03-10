import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=432263a67efa75df61533eb697839beb&&language=en-US".format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

import gdown

# Google Drive file IDs
movie_dict_file_id = "1WHfe3TyaMQ-kRv0d2pn-Imo3lKqk0_si"
similarity_file_id = "1P9pKIbWT3CVskdPSpu-aPkO1jqGskowh"


# Download files from Google Drive
gdown.download(f"https://drive.google.com/uc?id={movie_dict_file_id}", "movie_dict.pkl", quiet=False)
gdown.download(f"https://drive.google.com/uc?id={similarity_file_id}", "similarity.pkl", quiet=False)

# Load the files
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title("Movie Recommender System")

selected_movie_name = st.selectbox("What would you like to watch today?", movies['title'].values)

if st.button('Recommend'):
    names, poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(names[0])
        st.image(poster[0])

    with col2:
        st.write(names[1])
        st.image(poster[1])

    with col3:
        st.write(names[2])
        st.image(poster[2])

    with col4:
        st.write(names[3])
        st.image(poster[3])

    with col5:
        st.write(names[4])
        st.image(poster[4])

