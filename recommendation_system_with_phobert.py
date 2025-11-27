import numpy as np
import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel, AutoTokenizer
from underthesea import word_tokenize
import os

def get_sentence_embedding(model, tokenizer, sentence, device='cpu'):
    tokens = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True, max_length=256)
    tokens = {k: v.to(device) for k, v in tokens.items()}
    with torch.no_grad():
        outputs = model(**tokens)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.cpu().numpy()

def get_recommendation(ori_data, data, user_description, top_k=20, embedding_file_dir='anime_movies_embedding.npy'):
    if os.path.exists(embedding_file_dir):
        movie_embeddings = np.load(embedding_file_dir)
    else:
        movie_embeddings = []
        for content in data['movie_content_data']:
            emb = get_sentence_embedding(phobert, tokenizer, content)
            movie_embeddings.append(emb[0])
        movie_embeddings = np.array(movie_embeddings)
        np.save(embedding_file_dir, movie_embeddings)

    description_segmented = word_tokenize(user_description, format='text')
    query_embedding = get_sentence_embedding(phobert, tokenizer, description_segmented, device)

    # Tính cosine similarity
    similarities = cosine_similarity(query_embedding, movie_embeddings)[0]

    top_indices = similarities.argsort()[::-1][:top_k]

    return ori_data.iloc[top_indices]


if __name__ == '__main__':
    # Initialization
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    phobert = AutoModel.from_pretrained("vinai/phobert-base-v2").to(device)
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

    original_data = pd.read_csv('data/anime_movie.csv')
    anime_data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Nội Dung', 'Thể Loại', 'Rating'])
    # anime_data = pd.read_csv('MovieRecommendationSystem/data/anime_movie.csv', usecols=['Tên Phim', 'Nội Dung', 'Thể Loại', 'Rating'])

    ### Preprocessing
    # 1. Remove nan value of Rating
    anime_data = anime_data.dropna()
    anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.lower())
    anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.replace(' ', '_').replace(',', ' ') if isinstance(s, str) else s)
    # 2. Segment dataset

    anime_data['movie_content_data'] = anime_data['Tên Phim'] + " " + anime_data['Nội Dung'] + " " + anime_data['Thể Loại']
    anime_data['movie_content_data'] = anime_data['movie_content_data'].apply(lambda x: word_tokenize(x, format='text'))



    user_description = 'Hãy gợi ý các phim có chủ đề về tình yêu và học đường, có yếu tố siêu nhiên và siêu năng lực'
    recommendations = get_recommendation(original_data, anime_data, user_description, top_k=20)
    print(get_recommendation(original_data, anime_data, user_description))




