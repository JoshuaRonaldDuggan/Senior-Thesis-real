import pandas as pd
import numpy as np

class CollaborativeFiltering:
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df

    def cosine_similarity(self, target_ratings, other_ratings):
        dot_product = np.dot(target_ratings, other_ratings)
        mag_1 = np.sqrt(np.dot(target_ratings, target_ratings))
        mag_2 = np.sqrt(np.dot(other_ratings, other_ratings))
        return dot_product / (mag_1 * mag_2)

    def find_similar_users(self, target_user, similar_users=5):
        target_ratings = self.ratings_df[self.ratings_df['userId'] == target_user]
        similarity_scores = []

        for userId in self.ratings_df['userId'].unique():
            if userId != target_user:
                other_ratings = self.ratings_df[self.ratings_df['userId'] == userId]
                merged_df = pd.merge(target_ratings, other_ratings, on='movieId', suffixes=('_target', '_other'))

                if not merged_df.empty:
                    similarity = self.cosine_similarity(merged_df['scaled_rating_target'], merged_df['scaled_rating_other'])
                    similarity_scores.append((userId, similarity))

        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        return similarity_scores[:similar_users]

    def recommend_movies(self, target_user, recommendations=10):
        similar_users = self.find_similar_users(target_user)
        recommended_movies = {}

        for userId, _ in similar_users:
            user_ratings = self.ratings_df[self.ratings_df['userId'] == userId]

            for index, row in user_ratings.iterrows():
                movie_id = row['movieId']
                rating = row['scaled_rating']

                if movie_id not in recommended_movies:
                    recommended_movies[movie_id] = [rating]
                else:
                    recommended_movies[movie_id].append(rating)

        final_recommendations = [(movie, np.mean(ratings)) for movie, ratings in recommended_movies.items()]
        final_recommendations.sort(key=lambda x: x[1], reverse=True)

        final_recommendations = final_recommendations[:recommendations]

        return [int(movie[0]) for movie in final_recommendations]
