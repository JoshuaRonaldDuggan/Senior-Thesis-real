#This program takes in the ratings.csv file
#and creates a new csv file where each rating
#has the user's average rating subtracted from it.

import pandas as pd

file_path = r"C:\Users\Joshua\Senior Thesis\Programs\ratings.csv"

rating_df = pd.read_csv(file_path)

print(rating_df.head(10))

avg_rating_df = rating_df.groupby(by = ["userId"], as_index = False)['rating'].mean()

print(avg_rating_df.head())

merged_df = pd.merge(rating_df, avg_rating_df, on = 'userId', suffixes = ('', '_avg'))

merged_df['adjusted_rating'] = merged_df['rating'] - merged_df['rating_avg']

print(merged_df.head())

adjusted_rating_df = merged_df[['userId', 'movieId', 'timestamp' , 'adjusted_rating']]

print(adjusted_rating_df.head())