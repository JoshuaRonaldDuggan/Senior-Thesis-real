import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

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

    def recommend_movies(self, target_user, recommendations=5):
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

        return final_recommendations[:recommendations]

    def predict_rating(self, target_user, target_movie_id):
        similar_users = self.find_similar_users(target_user)

        weighted_sum = 0
        similarity_sum = 0

        for userId, similarity in similar_users:

            user_ratings = self.ratings_df[(self.ratings_df['userId'] == userId) & (self.ratings_df['movieId'] == target_movie_id)]


            if not user_ratings.empty:
                user_rating = user_ratings.iloc[0]['scaled_rating']
                weighted_sum += user_rating * similarity  
                similarity_sum += abs(similarity)  

        if similarity_sum == 0:
            return None
        else:
            return weighted_sum / similarity_sum





ratings_df = pd.read_csv(r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\filtered_ratings_small.csv")
cf = CollaborativeFiltering(ratings_df)
user_id = 1
recommendations = cf.predict_rating(user_id, 1263)
print(recommendations)
