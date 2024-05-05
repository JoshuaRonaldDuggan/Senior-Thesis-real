import pandas as pd
import numpy as np

class CollaborativeFiltering:
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df

    def cosine_similarity(self, target_ratings, other_ratings):
        dot_product = 0
        mag_1 = 0
        mag_2 = 0
        
        for rating_1, rating_2 in zip(target_rating, other_rating):
            weight = abs(target_rating) * abs(other_rating)

            dot_product += rating_1 * rating_2
            mag_1 += rating_1 ** 2
            mag_2 += rating_2 ** 2

        mag_1 = mag_1 ** 0.5
        mag_2 = mag_2 ** 0.5

        return dot_product / (mag_1 * mag_2) * weight 
        
        
    def find_similar_users(self, target_user, similar_users = 5):
        target_ratings = self.ratings_df[self.ratings_df['userId'] == target_user]

        similarity_scores = []

        for userId in self.ratings_df['userId'].unique():
            
            if userId != target_user:
                other_ratings = self.ratings_df[self.ratings_df['userId'] == userId]
                merged_df = pd.merge(target_ratings, other_ratings, on = 'movieId', suffixes = ('_target', "_other"))

                #We do this so we make sure that there is at least one movie in common betweent he target and other users
                if merged_df.empty == False:
                    similarity = self.cosine_similarity(merged_df['scaled_rating_target'], merged_df['scaled_rating_other'])
                    similarity_scores.append(userId, similarity)
        
        similarity_scores.sort(key = lambda x: x[1], reverse = True)
        return similarity_scores[: similar_users]
    
    def reccomend_movies(self, target_user, reccomendations = 5):
        similar_users = self.find_similar_users(target_user)

