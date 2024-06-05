import pandas as pd

file_path1 = r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\ratings_small.csv"


rating_df = pd.read_csv(file_path1)

rating_df = rating_df.drop(columns='timestamp')

movie_means = rating_df.groupby('movieId')['rating'].mean()

user_means  = rating_df.groupby('userId')['rating'].mean()

rating_df = rating_df.merge(movie_means, on = "movieId", suffixes= ('', '_movie'))
rating_df = rating_df.merge(user_means, on = "userId", suffixes= ('', '_user'))


rating_df['rating_adjusted'] = rating_df['rating'] - rating_df['rating_movie'] - rating_df['rating_user']

mean_adjusted_rating = rating_df['rating_adjusted'].mean()

rating_df['rating_adjusted'] -= mean_adjusted_rating

min_rating = rating_df['rating_adjusted'].min()
max_rating = rating_df['rating_adjusted'].max()


rating_df['scaled_rating'] = ((rating_df['rating_adjusted'] - min_rating) / (max_rating - min_rating)) * 2 - 1

filtered_df = rating_df[['userId', 'movieId', 'scaled_rating']]

output_path = r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\filtered_ratings_small.csv"

filtered_df.to_csv(output_path, index=False)
