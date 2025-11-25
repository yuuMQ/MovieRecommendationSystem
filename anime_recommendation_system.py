import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Content-based Recommendation System
def content_based_recommendation(data, user_movie, top_k=20, min_rating=8.0):
    filtered_data = data[data['Rating'] >= min_rating]
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(filtered_data['Thể Loại'])
    tfidf_matrix_to_dense = pd.DataFrame(data=tfidf_matrix.todense() ,index=filtered_data['Tên Phim'] ,columns=vectorizer.get_feature_names_out())

    cosine_sim = cosine_similarity(tfidf_matrix_to_dense)
    cosine_sim_to_dense = pd.DataFrame(data=cosine_sim, index=filtered_data['Tên Phim'], columns=filtered_data['Tên Phim'])

    movie_data = cosine_sim_to_dense.loc[user_movie, :]
    movie_data = movie_data.sort_values(ascending=False)[:top_k + 1]

    # Remove user movie
    movie_data = movie_data[movie_data.index != user_movie]

    return movie_data

def movies_detail(data, user_movie, recommendations):
    print("==================MOVIES RECOMMENDATION==========================")
    original_information = data[data['Tên Phim'] == user_movie].iloc[0]
    print("Phim gốc: \n{}".format(original_information))
    for i, (movie, similarity) in enumerate(recommendations.items(), 1):
        movie_info = data[data['Tên Phim'] == movie].iloc[0]
        print(movie_info)


def movies_info_list(data, user_movie, recommendations):
    rec_movies_list = {}





if __name__ == '__main__':
    original_data = pd.read_csv('data/anime_movie.csv')
    anime_data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating'])
    # anime_data = pd.read_csv('MovieRecommendationSystem/data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating'])

    ### Preprocessing
    # 1. Remove nan value of Rating
    anime_data = anime_data.dropna(subset=['Rating']).dropna(subset=['Thể Loại'])

    # 2. Replace ',' to ' ' of Thể Loại
    anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s)

    # # # Lọc theo tên Phim
    top_k = 20
    user_movie = 'Grand Blue'
    recommendations = content_based_recommendation(anime_data, user_movie, top_k=top_k)
    movies_detail(original_data, user_movie, recommendations)

