import pandas as pd
from content_based_filtering import ContentBasedFiltering
from collaborative_filtering import CollaborativeFiltering

movies_df = pd.read_csv(r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\keywords.csv")
ratings_df = pd.read_csv(r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\filtered_ratings_small.csv")
movies_metadata_df = pd.read_csv(r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\movies_metadata.csv", low_memory=False)
scaled_ratings_df = pd.read_csv(r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\scaled_user_generated_data.csv")



merged_ratings_df = pd.concat([ratings_df, scaled_ratings_df])


cb = ContentBasedFiltering(movies_df, merged_ratings_df)
cf = CollaborativeFiltering(merged_ratings_df)


def get_movie_titles(movie_ids, movies_metadata_df):
    return movies_metadata_df[movies_metadata_df['id'].astype(str).isin([str(mid) for mid in movie_ids])]['title'].tolist()

for user_id in scaled_ratings_df['userId'].unique():
    if user_id not in merged_ratings_df['userId'].unique():
        print(f"User ID {user_id} not found in merged ratings.")
        continue
    
    print(f"Trying {user_id} reccomendations.")
    content_based_recommendations = cb.recommend_movies(user_id)
    collaborative_recommendations = cf.recommend_movies(user_id)


    content_based_titles = get_movie_titles(content_based_recommendations, movies_metadata_df)
    collaborative_titles = get_movie_titles(collaborative_recommendations, movies_metadata_df)


    print(f"Algorithm A Recommendations for user {user_id}:", content_based_titles)
    print(f"Algorithm B Recommendations for user {user_id}:", collaborative_titles)
