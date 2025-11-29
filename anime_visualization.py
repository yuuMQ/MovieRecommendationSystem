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

    plt.figure(figsize=(10, 8))
    sns.barplot(data=top_20_rating, y='Tên Phim', x='Rating')
    plt.title('TOP 20 PHIM CÓ RATING CAO NHẤT')
    for i, value in enumerate(top_20_rating['Rating']):
        plt.text(value + 0.2, i, str(value), horizontalalignment='center')
    plt.show()

def create_histogram_of_rating(data):
    # Phân bố rating
    plt.figure(figsize=(8, 5))
    sns.histplot(data['Rating'], bins=20, kde=True)
    plt.title("PHÂN BỐ RATING")
    plt.show()



# data = pd.read_csv('MovieRecommendationSystem/data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating', 'Số lượng đánh giá', 'Năm Phát Hành'])
data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating', 'Số lượng đánh giá', 'Năm Phát Hành'])
data = data.dropna()
data['Thể Loại'] = data['Thể Loại'].apply(lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s)
data['Năm Phát Hành'] = data['Năm Phát Hành'].apply(extract_year)
data = data.dropna(subset=['Năm Phát Hành'])
data['Năm Phát Hành'] = pd.to_datetime(data['Năm Phát Hành'].astype(int), format='%Y')

top_20_votes = data.sort_values(by='Số lượng đánh giá', ascending=False)[:20]
sns.barplot(data=top_20_votes, y='Tên Phim', x='Số lượng đánh giá')
plt.title("TOP 20 PHIM CÓ LƯỢNG ĐÁNH GIÁ NHIỀU NHẤT")
plt.show()
