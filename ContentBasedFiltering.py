import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json

class ContentBasedFiltering:
    
    def __init__(self, movies_df, ratings_df):
        self.movies_df = movies_df
        self.ratings_df = ratings_df
        self.keywordProcess()
        self.make_vector()
        self.calculate_similarity()

    def keywordProcess(self):
        def inner_process(x):
            try:
                keywords = json.loads(x.replace("'", "\""))
                return ' '.join([word['name'] for word in keywords])
            except json.JSONDecodeError:
                return ''
        self.movies_df['keywords'] = self.movies_df['keywords'].apply(inner_process)

    def make_vector(self):
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df['keywords'])

    def calculate_similarity(self):
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def recommend_movies(self, user_id, k=10):
        user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id]

        if user_ratings.empty:
            print(f"No ratings found for userId {user_id}.")
            return pd.DataFrame()

        all_recommendations = {}

        for _, row in user_ratings.iterrows():
            movie_id = row['movieId']
            rating = row['scaled_rating']

            if movie_id not in self.movies_df['id'].values:
                continue
            
            i = self.movies_df[self.movies_df['id'] == movie_id].index[0]
            sim_scores = list(enumerate(self.cosine_sim[i]))
            sim_scores = [score for score in sim_scores if self.movies_df.iloc[score[0]]['id'] != movie_id]
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            for idx, score in sim_scores:
                sim_movie_id = self.movies_df.iloc[idx]['id']
                if sim_movie_id in all_recommendations:
                    all_recommendations[sim_movie_id] += score * rating
                else:
                    all_recommendations[sim_movie_id] = score * rating

        sorted_recommendations = sorted(all_recommendations.items(), key=lambda x: x[1], reverse=True)
        top_recommendations = sorted_recommendations[:k]

        recommended_movies = self.movies_df[self.movies_df['id'].isin([rec[0] for rec in top_recommendations])]
        recommended_movies['weighted_score'] = recommended_movies['id'].map(dict(top_recommendations))

        return recommended_movies[['id', 'weighted_score']].sort_values(by='weighted_score', ascending=False)

movies_df = pd.read_csv(r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\keywords.csv")
ratings_df = pd.read_csv(r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\filtered_ratings_small.csv")

cb = ContentBasedFiltering(movies_df, ratings_df)

user_id = 1
recommendations = cb.recommend_movies(user_id)
print(recommendations)
