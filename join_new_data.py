import pandas as pd

def create_movie_ratings_df(df, movies_metadata_df):
    if 'Timestamp' not in df.columns or 'userId' not in df.columns:
        raise KeyError("Required columns 'Timestamp' or 'userId' not found in DataFrame")

    ratings_df = df.melt(id_vars=["Timestamp", "userId"],
                         var_name="movieTitle", value_name="rating")
    
    ratings_df = ratings_df.dropna(subset=["rating"])

    ratings_df = ratings_df.merge(movies_metadata_df, left_on="movieTitle", right_on="title")

    ratings_df = ratings_df[["userId", "id", "rating"]].rename(columns={"id": "movieId"})

    ratings_df = ratings_df.sort_values(by="userId")

    return ratings_df

testing_path = r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\Movie_recs.csv"
testing_df = pd.read_csv(testing_path)


testing_df = testing_df.rename(columns={"Please enter your name / screen name (final data will be anonymous, only for purposes of sending you proper list of recommendations). ": "userId"})


movies_metadata_path = r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\movies_metadata.csv"
movies_metadata_df = pd.read_csv(movies_metadata_path, low_memory=False)

try:
    movie_ratings_df = create_movie_ratings_df(testing_df, movies_metadata_df)

    print("Movie Ratings DataFrame:")
    print(movie_ratings_df.head())

    movie_ratings_df['movieId'] = movie_ratings_df['movieId'].astype(int)

    output_path = r"C:\Users\Joshua\Senior Thesis\Programs\Senior-Thesis-real\user_generated_data.csv"
    movie_ratings_df.to_csv(output_path, index=False)

    print(f"Data saved to {output_path}")
except KeyError as e:
    print(f"Error: {e}")
