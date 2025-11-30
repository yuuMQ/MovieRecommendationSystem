# Movie Recommendation System

---
## 1. Anime Movies Recommendation System:
### a. Movie Web Link: https://animehay.life/
### b. Report: 
![HighestRating](MovieRecommendationSystem/assets/HighestRating.png)
![HighestVotes](MovieRecommendationSystem/assets/HighestVotes.png)
![RatingDistribution](MovieRecommendationSystem/assets/RatingDistribution.png)
![NumberOfMovies](MovieRecommendationSystem/assets/NumberOfMovies.png)
![Genres](MovieRecommendationSystem/assets/Genres.png)
![RatingAndVotes](MovieRecommendationSystem/assets/RatingAndVotes.png)

### c. Method:

- Anime dataset was scraped from an anime web (Hope there will be no license problem :)) )
- Scrapy was used to collect anime dataset. **[Details](https://github.com/yuuMQ/MovieRecommendationSystem/blob/main/MovieScraper/MovieScraper/spiders/anime_movie_scraper.py)**
- We use a ***Content-based recommendation System*** for anime movies dataset:
- *'Thể Loại'*, *'Nội Dung'* and *'Tên Phim'* features are merged into a *'movie_content_data' feature.  
- The recommendation System has two different methods:
  - TF-IDF
  - PhoBert
### d. Dataflow:
![image](assets/MovieRecDataFlow.drawio.png)


### e. Demo:

--- 
## 2. Vietnamese and Other Movies Recommendation System: ***TO BE CONTINUE***
### a. Movie Web Link: https://phimmoi15.net/
### b. Report:
### c. Demo:

---

## Team Members:
- 2351010176 - Phạm Minh Quân
- 2351010238 - Lê Khắc Tùng
