import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pprint import pprint
from underthesea import word_tokenize

# Content-based Recommendation System
def content_based_recommendation(data, user_description, top_k=20):
    vectorizer = TfidfVectorizer()

    user_description = word_tokenize(user_description, format='text')

    movie_content_matrix = vectorizer.fit_transform(data['movie_content_data'])
    user_description_matrix = vectorizer.transform([user_description])

    cosine_sim = cosine_similarity(movie_content_matrix, user_description_matrix).flatten()
    top_indices = cosine_sim.argsort()[::-1][:top_k]
    movie_data = anime_data.iloc[top_indices]

    return movie_data['Tên Phim'].tolist()

def movies_info_list(ori_data, recommendations):
    rec_movies_list = []
    for movie in recommendations:
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
    with open('vietnamese-stopwords.txt', 'r', encoding='utf-8') as f:
        stop_words = [w.strip() for w in f.readlines()]

    original_data = pd.read_csv('data/anime_movie.csv')
    # original_data = pd.read_csv('MovieRecommendationSystem/data/anime_movie.csv')
    anime_data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Nội Dung', 'Thể Loại', 'Rating'])
    # anime_data = pd.read_csv('MovieRecommendationSystem/data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating'])

    ### Preprocessing
    # 1. Remove nan value of Rating
    anime_data = anime_data.dropna()

    # 2. Replace ',' to ' ' of Thể Loại
    anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s)
    anime_data['movie_content_data'] = anime_data['movie_content_data'] = anime_data['Tên Phim'] + " " + anime_data['Nội Dung'] + " " + anime_data['Thể Loại']
    anime_data['movie_content_data'] = anime_data['movie_content_data'].apply(lambda x: word_tokenize(x, format='text'))

    vectorizer = TfidfVectorizer(stop_words=stop_words)
    user_input = 'Gợi ý tôi phim có nội dung về nhân vật chính chuyển sinh vào thế giới khác có sức mạnh phi thường và đồng hành cùng dàn harem xinh đẹp'


    # Vectorizer - vector hóa
    recommendations = content_based_recommendation(anime_data, user_input)
    pprint(movies_info_list(original_data, recommendations))
