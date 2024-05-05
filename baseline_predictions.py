import pandas as pd

file_path = r"C:\Users\Joshua\Senior Thesis\Programs\ratings.csv"

rating_df = pd.read_csv(file_path)

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



rating_df['scaled_rating'] = ((rating_df['rating_adjusted'] - min_rating) / (max_rating - min_rating))

print(rating_df)

