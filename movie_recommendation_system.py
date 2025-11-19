import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_recommendation(user_movie, df, top_k):
    data = df.loc[user_movie, :]
    data = data.sort_values(ascending=False)[:top_k]
    return data

# data = pd.read_csv('MovieRecommendationSystem/data/phimmoi_movies_data.csv', usecols=['name', 'genres', 'rating', 'year'])
data = pd.read_csv('data/phimmoi_movies_data.csv', usecols=['name', 'genres', 'rating', 'year'])
data['rating'] = data['rating'].replace('N/a', None)
data['rating'] = pd.to_numeric(data['rating'], errors='coerce')
data = data.dropna(subset=['rating'])

data['genres'] = data['genres'].apply(lambda x: x.replace(' ', '').replace(',', ' '))

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(data['genres'])
tfidf_matrix_dense = pd.DataFrame(tfidf_matrix.todense(), index=data['name'], columns=vectorizer.get_feature_names_out())

cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim_dense = pd.DataFrame(cosine_sim, index=data['name'], columns=data['name'])
input_text = 'Huyền Thoại La Tiểu Hoắc'
print(get_recommendation(input_text, cosine_sim_dense, top_k=20))
