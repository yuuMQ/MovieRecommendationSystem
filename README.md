# Movie Recommendation System

---
## 1. Anime Movies Recommendation System:
### a. Movie Web Link: https://animehay.life/
### b. Report: 
### c. Method:

- Anime dataset was scraped from an anime web (Hope there will be no license problem :)) )
- Scrapy was used to collect anime dataset. **[Details](https://github.com/yuuMQ/MovieRecommendationSystem/blob/main/MovieScraper/MovieScraper/spiders/anime_movie_scraper.py)**
- We use a ***Content-based recommendation System*** for anime movies dataset:
  - TF-IDF combined with Cosine Similarity on **Thể Loại** feature.
  - Filtered by top-rated - **Rating** feature (rating >= 8.0 - This value can be adjusted).
  - Recommend 20 anime movies that are the most similar to the user-selected movie. 
### d. Demo:

--- 
## 2. Vietnamese and Other Movies Recommendation System:
### a. Movie Web Link: https://phimmoi15.net/
### b. Report:
### c. Demo:

---

## Team Members:
- 2351010176 - Phạm Minh Quân
- 2351010238 - Lê Khắc Tùng
