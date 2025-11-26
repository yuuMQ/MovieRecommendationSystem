import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# data = pd.read_csv('MovieRecommendationSystem/data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating', 'Số lượng đánh giá', 'Năm Phát Hành'])
data = pd.read_csv('data/anime_movie.csv', usecols=['Tên Phim', 'Thể Loại', 'Rating', 'Số lượng đánh giá', 'Năm Phát Hành'])
data = data.dropna(subset=['Rating']).dropna(subset=['Thể Loại'])
data['Thể Loại'] = data['Thể Loại'].apply(lambda s: s.replace(' ', '').replace(',', ' ') if isinstance(s, str) else s)

# Bar Chart -> Top 20 Most Rating Movies
top20_data = data.sort_values(by=['Rating'], ascending=False)[:20]

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
bars = plt.barh(range(len(top20_data)), top20_data['Rating'])
plt.yticks(range(len(top20_data)), top20_data['Tên Phim'])
plt.title("TOP 20 Anime Có Rating Cao Nhất Dựa Trên Rating Của Animehay", fontsize=16, fontweight='bold')
plt.xlabel('Rating')
plt.ylabel('Tên Phim')
plt.show()
# Histogram -> Phân bố Rating