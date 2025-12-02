import streamlit as st
import pandas as pd
from anime_recommendation_system import content_based_recommendation, movies_info_list as movies_info_tfidf
from recommendation_system_with_transformers import get_recommendation as transformer_get_recommendation, movies_info_list as movies_info_transformer
from underthesea import word_tokenize


original_data = pd.read_csv('data/anime_movie.csv')
anime_data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Nội Dung', 'Thể Loại', 'Rating', 'Image'])
anime_data = anime_data.dropna()
anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s)
anime_data['movie_content_data'] = anime_data['movie_content_data'] = anime_data['Tên Phim'] + " " + anime_data['Nội Dung'] + " " + anime_data['Thể Loại']
anime_data['movie_content_data'] = anime_data['movie_content_data'].apply(lambda x: word_tokenize(x, format='text'))

st.set_page_config(page_title="Anime Recommendation System", layout="wide")
st.title("Hệ Thống Gợi Ý Phim Anime ")

method = st.radio(
    "Chọn phương pháp gợi ý:",
    ("TF-IDF", "Transformer")
)
top_k = st.slider("Số lượng phim gợi ý:", 5, 30, 10)

user_query = st.text_area(
    "Nhập mô tả nội dung phim mong muốn:",
    height=120
)

def display_movie(movie):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(movie['Image'], width=250)
    with col2:
        st.markdown(f"### {movie['Tên Phim']}")
        st.write(f"**Thể loại:** {movie['Thể Loại']}")
        st.write(f"**Rating:** {movie['Rating']}")
        with st.expander("Xem nội dung chi tiết"):
            st.write(movie['Nội Dung'])

if st.button("Gợi Ý Ngay"):
    if user_query.strip() == "":
        st.warning("Vui lòng nhập mô tả phim!")
        st.stop()

    with st.spinner("Đang tìm phim phù hợp..."):
        if method == "TF-IDF":
            rec_titles = content_based_recommendation(anime_data, user_query, top_k)
            recommendations = movies_info_tfidf(original_data, rec_titles)
        else:
            rec_titles = transformer_get_recommendation(original_data, user_query, top_k)
            recommendations = movies_info_transformer(original_data, rec_titles)

    st.subheader("Các phim gợi ý:")
    for movie in recommendations:
        display_movie(movie)
