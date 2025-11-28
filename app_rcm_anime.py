'''
    Sửa lại nhé !!!!!!!


'''

import streamlit as st
import pandas as pd
from anime_recommendation_system import content_based_recommendation, movies_info_list   # import từ file bạn đã viết

original_data = pd.read_csv('data/anime_movie.csv')
anime_data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating'])
anime_data = anime_data.dropna(subset=['Rating']).dropna(subset=['Thể Loại'])
anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s)
st.title("🎬 Hệ Thống Gợi Ý Phim")
st.write("Hệ thống gợi ý dựa trên thể loại nội dung (Content-Based Filtering)")


user_movie = st.selectbox("Chọn một bộ phim bạn thích:", anime_data['Tên Phim'].tolist())

top_k = st.slider("Số lượng phim gợi ý:", 5, 30, 10)

if st.button("Gợi Ý Ngay 🚀"):
    with st.spinner("Đang phân tích dữ liệu..."):
        recommendations = content_based_recommendation(anime_data, user_movie, top_k)
        movie_list = movies_info_list(original_data, recommendations)

    st.subheader(f" Các phim giống với: **{user_movie}**")

    for movie in movie_list:
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                if pd.notna(movie['Image']):
                    st.image(movie['Image'], use_container_width=True)
                else:
                    st.write("No Image")

            with col2:
                st.markdown(f"### 🎞️ {movie['Tên Phim']}")
                if pd.notna(movie['Tên Khác']) and movie['Tên Khác'].strip() != "":
                    st.write(f"**Tên khác:** {movie['Tên Khác']}")
                st.write(f"**Thể loại:** {movie['Thể Loại']}")
                st.write(f"**Rating:** ⭐ {movie['Rating']}")
                st.write(f"**Năm phát hành:** {movie['Năm Phát Hành']}")
                st.write(movie['Nội Dung'])