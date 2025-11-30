import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re

def extract_year(year):
    year = str(year)
    digits = re.findall(r'\d{4}', year)
    if digits:
        return int(digits[0])
    return None


def create_top20_highest_rating_movie(data):
    # Thống kê 20 bộ phim có rating cao nhất
    top_20_rating = data.sort_values(by='Rating', ascending=False)[:20]

    plt.figure(figsize=(24, 6))
    # sns.barplot(data=top_20_rating, y='Tên Phim', x='Rating')
    plt.barh(top_20_rating['Tên Phim'], top_20_rating['Rating'])
    plt.xlabel('Rating')
    plt.ylabel('Tên Phim')
    plt.title('TOP 20 PHIM CÓ RATING CAO NHẤT')
    plt.tight_layout()
    plt.show()

def create_histogram_of_rating(data):
    # Phân bố rating
    plt.figure(figsize=(8, 5))
    sns.histplot(data['Rating'], bins=20, kde=True)
    plt.title("PHÂN BỐ RATING")
    plt.show()

def create_top20_highest_votes_movie(data):
    top_20_votes = data.sort_values(by='Số lượng đánh giá', ascending=False)[:20]
    plt.figure(figsize=(24, 6))
    # sns.barplot(data=top_20_votes, y='Tên Phim', x='Số lượng đánh giá')
    plt.barh(top_20_votes['Tên Phim'], top_20_votes['Số lượng đánh giá'])
    plt.xlabel("Số lượng đánh giá")
    plt.ylabel("Tên Phim")
    plt.title("TOP 20 PHIM CÓ SỐ LƯỢNG ĐÁNH GIÁ NHIỀU NHẤT")
    plt.tight_layout()
    plt.show()

def create_number_of_movies_year_more_than_10(data):
    year_count = data['Năm Phát Hành'].value_counts().sort_index()
    year_count = year_count[year_count.values >= 10]
    year_count.index = year_count.index.astype(int)
    plt.figure(figsize=(14, 6))
    sns.barplot(x=year_count.index, y=year_count.values)
    plt.title("SỐ LƯỢNG PHIM PHÁT HÀNH THEO NĂM TRÊN TRANG WEB (SỐ PHIM PHẢI >= 10)")
    plt.xlabel("Năm Phát Hành")
    plt.ylabel("Số Lượng Đánh Giá")
    plt.show()

def create_genres_plot(data):
    genres = data['Thể Loại'].str.split(' ', expand=True).stack()
    genres_count = genres.value_counts()
    genres_count = genres_count[genres_count.index != 'Anime']
    genres_count = genres_count[genres_count.index != '[CNA]_Hài_hước']
    plt.figure(figsize=(10, 6))
    sns.barplot(x=genres_count.values, y=genres_count.index)
    plt.title("THỐNG KÊ THỂ LOẠI PHIM PHỔ BIẾN")
    plt.show()

def create_line_chart_with_rating_and_votes(data):
    rating_by_year = data.groupby("Năm Phát Hành")['Rating'].mean()
    votes_by_year = data.groupby("Năm Phát Hành")['Số lượng đánh giá'].mean()

    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Rating
    color = 'teal'
    ax1.set_xlabel('Năm')
    ax1.set_ylabel("Rating trung bình", color=color)
    line1 = ax1.plot(rating_by_year.index, rating_by_year.values, color=color, marker='o', label='Rating Trung Bình')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', linewidth=0.6)

    # Votes
    ax2 = ax1.twinx()
    color = 'coral'
    ax2.set_ylabel("Số lượng đánh giá trung bình", color=color)
    line2 = ax2.plot(votes_by_year.index, votes_by_year.values, color=color, marker='o', label='Số Lượng Đánh Giá Trung Bình')

    plt.title("BIẾN ĐỘNG RATING VÀ VOTES THEO NĂM")
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    plt.show()

# def create_dashboard(data):
#     top_20_rating = data.sort_values(by='Rating', ascending=False)[:20]
#     top_20_votes = data.sort_values(by='Số lượng đánh giá', ascending=False)[:20]
#
#     year_count = data['Năm Phát Hành'].value_counts().sort_index()
#     year_count = year_count[year_count.values >= 10]
#     year_count.index = year_count.index.astype(int)
#
#     genres = data['Thể Loại'].str.split(' ', expand=True).stack()
#     genres_count = genres.value_counts()
#     genres_count = genres_count[genres_count.index != 'Anime']
#     genres_count = genres_count[genres_count.index != '[CNA]_Hài_hước']
#
#     rating_by_year = data.groupby("Năm Phát Hành")['Rating'].mean()
#     votes_by_year = data.groupby("Năm Phát Hành")['Số lượng đánh giá'].mean()
#
#     # Draw subplots in 1 figure
#     fig = plt.figure(figsize=(24, 30))
#
#     # 1. Top 20 movies with Rating
#     ax1 = plt.subplot(4, 2, 1)
#     sns.barplot(data=top_20_rating, y='Tên Phim', x='Rating', ax=ax1)
#     for i, value in enumerate(top_20_rating['Rating']):
#         plt.text(value + 0.2, i, str(value), horizontalalignment='center')
#     ax1.set_title('TOP 20 PHIM CÓ RATING CAO NHẤT')
#
#     # 2. Top 20 movies with Votes
#     ax2 = plt.subplot(4, 2, 2)
#     sns.barplot(data=top_20_votes, y='Tên Phim', x='Số lượng đánh giá', ax=ax2)
#     for i, value in enumerate(top_20_rating['Rating']):
#         plt.text(value + 0.2, i, str(value), horizontalalignment='center')
#     ax1.set_title('TOP 20 PHIM CÓ SỐ LƯỢNG ĐÁNH GIÁ NHIỀU NHẤT')
#
#     # 3. Rating Distribution
#     ax3 = plt.subplot(4, 2, 3)
#     sns.histplot(data['Rating'], bins=20, kde=True, ax=ax3)
#     ax2.set_title('Phân Bố Rating')
#
#     # 4. Number of Movies each year
#     ax4 = plt.subplot(4, 2, 4)
#     sns.barplot(x=year_count.index, y=year_count.values, ax=ax4)
#     ax4.set_xlabel('Năm')
#     ax4.set_ylabel('Số lượng phim')
#     ax4.set_title('SỐ LƯỢNG PHIM MỖI NĂM (SỐ LƯỢNG PHIM >= 10)')
#     plt.setp(ax4.get_xticklabels(), rotation=45)
#
#     # 5. The population of genres
#     ax5 = plt.subplot(4, 2, 5)
#     sns.barplot(x=genres_count.index, y=genres_count.values, ax=ax5)
#     ax5.set_title('Thể Loại Phim Phổ Biến')
#     ax5.set_xlabel('Số lượng phim')
#
#     # Rating and Votes each year
#     ax6 = plt.subplot(4, 2, (7, 8))
#     color1 = 'teal'
#     ax6_twin = ax6.twinx()
#     line1 = ax6.plot(rating_by_year.index, rating_by_year.values, color=color1, marker='o', linewidth=2.5, label='Rating trung bình')
#     ax6.set_ylabel('Rating trung bình')
#     ax6.tick_params(axis='y', labelcolor=color1)
#
#     color2 = 'coral'
#     line2 = ax6_twin.plot(votes_by_year.index, votes_by_year.values, color=color2, marker='o', linewidth=2.6, label='Số lượng đánh giá trung bình')
#     ax6_twin.set_ylabel("Số lượng đánh giá trung bình")
#     ax6_twin.tick_params(axis='y', labelcolor=color2)
#
#     ax6.set_title("Biến động Rating và Votes mỗi năm")
#     ax6.set_xlabel("Năm")
#
#     lines = line1 + line2
#     labels =[l.get_label() for l in lines]
#     ax6.legend(lines, labels, loc='upper left')
#
#     plt.suptitle("ANIME MOVIE DASHBOARD")
#     plt.show()



if __name__ == '__main__':
    data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating', 'Số lượng đánh giá', 'Năm Phát Hành'])
    data = data.dropna()
    data['Thể Loại'] = data['Thể Loại'].apply(lambda s: s.replace(' ', '_').replace(',', ' ') if isinstance(s, str) else s)
    data['Năm Phát Hành'] = data['Năm Phát Hành'].apply(extract_year)
    data = data.dropna(subset=['Năm Phát Hành'])


    create_top20_highest_votes_movie(data)
    create_number_of_movies_year_more_than_10(data)
    create_genres_plot(data)
    create_line_chart_with_rating_and_votes(data)
    create_top20_highest_rating_movie(data)
    create_histogram_of_rating(data)