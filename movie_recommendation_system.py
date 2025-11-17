import pandas as pd


# Read Data
data = pd.read_csv('data/anime_movie.csv')

# Preprocessing
# 1. Remove NaN of Rating column
data = data.dropna(subset=['Rating'])