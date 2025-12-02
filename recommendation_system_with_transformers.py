import numpy as np
import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from underthesea import word_tokenize
import os
from pprint import pprint

def get_sentence_embedding(sentences, device):
    embeddings = model.encode(
        sentences,
        batch_size=128,
        show_progress_bar=True,
        normalize_embeddings=True,
        device=device
    )
    return embeddings

def get_recommendation(data, user_description, top_k=20, embedding_file_dir='anime_movies_embedding.npy'):
    if os.path.exists(embedding_file_dir):
        movie_embeddings = np.load(embedding_file_dir)
    else:
        contents = data['movie_content_data'].tolist()
        movie_embeddings = get_sentence_embedding(contents, device=device)
        movie_embeddings = np.array(movie_embeddings)
        np.save(embedding_file_dir, movie_embeddings)

    description_segmented = word_tokenize(user_description, format='text')
    query_embedding = get_sentence_embedding([description_segmented], device=device)

    # Tính cosine similarity
    similarities = cosine_similarity(query_embedding, movie_embeddings)[0]

    top_indices = similarities.argsort()[::-1][:top_k]
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


# Initialization
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('keepitreal/vietnamese-sbert')
anime_data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Nội Dung', 'Thể Loại', 'Rating'])

if __name__ == '__main__':
    original_data = pd.read_csv('data/anime_movie.csv')

    ### Preprocessing
    # 1. Remove nan value of Rating
    anime_data = anime_data.dropna()
    anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.lower())
    anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.replace(' ', '_').replace(',', ' ') if isinstance(s, str) else s)
    # 2. Segment dataset

    anime_data['movie_content_data'] = anime_data['Tên Phim'] + " " + anime_data['Nội Dung'] + " " + anime_data['Thể Loại']
    # anime_data['movie_content_data'] = anime_data['movie_content_data'].apply(lambda x: word_tokenize(x, format='text'))

    user_description = 'Phim có chủ đề về nam sinh bị dịch chuyển sang dị giới cùng bạn bè và bị phản bội'

    recommendations = get_recommendation(anime_data, user_description, top_k=20)
    pprint(movies_info_list(original_data, recommendations))




