import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Item-based Collaborative Filtering


def get_recommendation(user_movie, df, num):
    data = df.loc[user_movie, :]
    data = data.sort_values(ascending=False)[:num]
    return data

anime_data = pd.read_csv('data/anime_movie.csv')

# Preprocessing
# 1. Remove nan value of Rating
anime_data = anime_data.dropna(subset=['Rating']).dropna(subset=['Thể Loại'])

# 2. Replace nan to '' of Tên Khác
anime_data['Tên Khác'] = anime_data['Tên Khác'].replace(np.nan, '')

# 3. Replace ',' to ' ' of Thể Loại
anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s)

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(anime_data['Thể Loại'])
tfidf_matrix_to_dense = pd.DataFrame(tfidf_matrix.todense(), index=anime_data['Tên Phim'], columns=vectorizer.get_feature_names_out())

cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim_dense = pd.DataFrame(cosine_sim, index=anime_data['Tên Phim'], columns=anime_data['Tên Phim'])

# # # Lọc theo tên Phim
top_k = 20
user_movie = 'Boku no Hero Academia the Movie: Futari no Hero'
# print(get_recommendation(user_movie, cosine_sim_dense, top_k))

