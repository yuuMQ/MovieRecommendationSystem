import streamlit as st
import pandas as pd

# Import 2 hệ thống gợi ý
from anime_recommendation_system import content_based_recommendation, movies_info_list
from recommendation_system_with_phobert import get_recommendation

# Load dữ liệu
original_data = pd.read_csv('data/anime_movie.csv')
anime_data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating'])
anime_data = anime_data.dropna(subset=['Rating']).dropna(subset=['Thể Loại'])
anime_data['Thể Loại'] = anime_data['Thể Loại'].apply(
    lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s
)

st.set_page_config(page_title="Hệ Thống Gợi Ý Anime", layout="wide")

st.title("Hệ Thống Gợi Ý Phim Anime")
# st.write("Bạn muuốn gợi ý dựa trên : :")
mode = st.radio(
    "Bạn muuốn gợi ý dựa trên :",
    ("Thể loại phim", "Nội dung")
)

top_k = st.slider("Số lượng phim gợi ý:", 5, 30, 10)

# ================= OPTION 1 ======================
if mode == "Thể loại phim":
    st.subheader("Chọn hoặc tìm phim bạn yêu thích")
    user_movie = st.selectbox("Phim:", anime_data['Tên Phim'].tolist())

    if st.button("Gợi Ý Ngay", key="btn1"):
        with st.spinner("Đang tìm các phim tương tự..."):
            rec = content_based_recommendation(anime_data, user_movie, top_k)
            movie_list = movies_info_list(original_data, rec)

        st.subheader(f"Phim giống với **{user_movie}**:")
        for movie in movie_list:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(movie['Image'], width=200)
                with col2:
                    st.markdown(f"### {movie['Tên Phim']}")
                    if pd.notna(movie['Tên Khác']):
                        st.write(f"**Tên khác:** {movie['Tên Khác']}")
                    st.write(f"**Thể loại:** {movie['Thể Loại']}")
                    st.write(f"**Rating:**  {movie['Rating']}")
                    st.write(f"**Năm phát hành:** {movie['Năm Phát Hành']}")
                    st.write(movie['Nội Dung'])

else:
    st.subheader("Nhập mô tả nội dung bạn muốn xem")

    user_query = st.text_area(
        "Ví dụ: *phim tình cảm học đường có yếu tố phép thuật và siêu năng lực*",
        height=200
    )

    if st.button("Gợi Ý Theo Nội Dung", key="btn2"):
        if user_query.strip() == "":
            st.warning("Vui lòng nhập mô tả phim!")
        else:
            with st.spinner("Đang tìm phim phù hợp..."):
                rec_movies = get_recommendation(original_data, anime_data, user_query, top_k)

            st.subheader("Kết quả phù hợp nhất với mô tả của bạn:")
            for _, movie in rec_movies.iterrows():
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.image(movie['Image'],  width=200)
                    with col2:
                        st.markdown(f"###  {movie['Tên Phim']}")
                        if pd.notna(movie['Tên Khác']):
                            st.write(f"**Tên khác:** {movie['Tên Khác']}")
                        st.write(f"**Thể loại:** {movie['Thể Loại']}")
                        st.write(f"**Rating:** {movie['Rating']}")
                        st.write(f"**Năm phát hành:** {movie['Năm Phát Hành']}")
                        st.write(movie['Nội Dung'])
