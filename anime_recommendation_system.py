import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pprint import pprint

# Content-based Recommendation System
def content_based_recommendation(ori_data, data, user_movie, top_k=20):
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(data['Thể Loại'])
    tfidf_matrix_to_dense = pd.DataFrame(data=tfidf_matrix.todense(), index=data['Tên Phim'], columns=vectorizer.get_feature_names_out())

    cosine_sim = cosine_similarity(tfidf_matrix_to_dense)
    cosine_sim_to_dense = pd.DataFrame(data=cosine_sim, index=data['Tên Phim'], columns=data['Tên Phim'])
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


def movies_info_list(ori_data, recommendations):
    '''
        movies list format:
        [{
            Tên Phim:
            Tên Khác:
            Nội Dung:
            Thể Loại:
            Rating:
            Số lượng đánh giá:
            Năm Phát Hành:
            Image:
        },
        ...
        ]
    '''
    rec_movies_list = []
    for i, movie in enumerate(recommendations.index):
        movie_details = ori_data[ori_data['Tên Phim'] == movie].iloc[0]

        movie_list_info = {
            'Tên Phim': movie_details['Tên Phim'],
            'Tên Khác': movie_details['Tên Khác'],
            'Nội Dung': movie_details['Nội Dung'],
            'Thể Loại': movie_details['Thể Loại'],
            'Rating': movie_details['Rating'],
            'Số lượng đánh giá': movie_details['Số lượng đánh giá'],
            'Năm Phát Hành': movie_details['Năm Phát Hành'],
            'Image': movie_details['Image']
        }
        rec_movies_list.append(movie_list_info)

    return rec_movies_list



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
    recommendations = content_based_recommendation(original_data, anime_data, user_movie, top_k=top_k)
    # movies_detail(original_data, user_movie, recommendations)
    movie_list = movies_info_list(original_data, recommendations)
    pprint(movie_list)
