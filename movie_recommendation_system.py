import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pprint import pprint
import re
from sentence_transformers import SentenceTransformer

# Content-based Recommendation System
def content_based_recommendation(data, user_movie, top_k=20):
    pass

def get_recommendation(user_movie, df, top_k=20):
    data = df.loc[user_movie, :]
    data = data.sort_values(ascending=False)[: top_k+1]
    return data

if __name__ == '__main__':
    with open('vietnamese-stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords_list= [word.strip() for word in f.readlines()]
    # with open('MovieRecommendationSystem/vietnamese-stopwords.txt', 'r', encoding='utf-8') as f:
    #     stopwords_list= [word.strip() for word in f.readlines()]

    # original_data = pd.read_csv('data/anime_movie.csv')
    # original_data = pd.read_csv('MovieRecommendationSystem/data/anime_movie.csv')
    anime_data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Nội Dung', 'Thể Loại', 'Rating'])
    # anime_data = pd.read_csv('MovieRecommendationSystem/data/anime_movie.csv', usecols=['Tên Phim', 'Nội Dung', 'Thể Loại', 'Rating'])

    ### Preprocessing
    # 1. Remove nan value of Rating
    anime_data = anime_data.dropna()

    # 2. Replace ',' to ' ' of Thể Loại
    anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s)

    anime_data['movie_content_data'] = anime_data['Tên Phim'] + " " + anime_data['Nội Dung'] + " " + anime_data['Thể Loại']

    model = SentenceTransformer("all-MiniLM-L6-v2")
    content_embedding = model.encode(anime_data['movie_content_data'].tolist(), convert_to_tensor=False, show_progress_bar=True)


