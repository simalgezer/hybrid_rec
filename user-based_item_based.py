#preparing data 
def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv("/kaggle/input/movielens-20m-dataset/movie.csv")
    rating = pd.read_csv("/kaggle/input/movielens-20m-dataset/rating.csv")
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()

user_movie_df.head(50)

#Selecting A Random User and Finding the Random User’s Watched Movies (User-based Recommendation Part 1)
random_user = int(pd.Series(user_movie_df.index).sample(1, random_state=45).values)
#28941

random_user_df = user_movie_df[user_movie_df.index == random_user]
random_user_df.head()

random_user_df.notna().any()
random_user_df.columns[random_user_df.notna().any()]
type(random_user_df.columns[random_user_df.notna().any()])  
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
movies_watched[0:10]

#Finding Other Users (User-based Recommendation Part 2)
len(movies_watched) #33

movies_watched_df = user_movie_df[movies_watched]  
movies_watched_df.head()
movies_watched_df.T.head()

user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count.head()

user_movie_count = user_movie_count.reset_index()
user_movie_count.head()
user_movie_count.columns = ["userId", "movie_count"]
user_movie_count.sort_values(by="movie_count", ascending=False)

perc = len(movies_watched) * 70 / 100
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]
users_same_movies.head()


#Finding Correlation between Sarah’s and Other Users’ Common Watched Movies (User-based Recommendation Part 3)
final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                      random_user_df[movies_watched]])

final_df.head()
final_df.shape
final_df.T.corr()

corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()
corr_df.head()

top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][
    ["user_id_2", "corr"]].reset_index(drop=True)
top_users = top_users.sort_values(by='corr', ascending=False)
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

rating = pd.read_csv("/kaggle/input/movielens-20m-dataset/rating.csv")
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]
top_users_ratings.head()

#Adding Weighted Rating & Recommending 5 Movies (User-based Recommendation Part 4)
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
top_users_ratings.head()
top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})

recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
recommendation_df.head()
recommendation_df = recommendation_df.reset_index()

recommendation_df[recommendation_df["weighted_rating"] > 3.5]
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating", ascending = False)
movies_to_be_recommend.head()

movie = pd.read_csv ("/kaggle/input/movielens-20m-dataset/movie.csv")
recommended_user_based_df = movies_to_be_recommend.merge (movie[["movieId", "title"]])
recommended_user_based_df.head()
recommended_user_based_df.shape #(32,3)

recommended_user_based_df = recommended_user_based_df.loc[~recommended_user_based_df["title"].isin(movies_watched)][:5]


#Finding the Item (Item-based Recommendation Part 1)
movie = pd.read_csv("/kaggle/input/movielens-20m-dataset/movie.csv")
rating = pd.read_csv("/kaggle/input/movielens-20m-dataset/rating.csv")
user = 28941

movie_id = rating[(rating["userId"] == user) & (rating["rating"] == 5.0)]. \
               sort_values (by="timestamp", ascending=False)["movieId"][0:1].values[0]

movie.loc[movie["movieId"] == movie_id, "title"]

#Finding Correlation between Sarah’s and Other Users’ Common Watched Movies (Item-based Recommendation Part 2)
def item_based_recommender(movie_name, user_movie_df, head=10):
    movie = user_movie_df[movie_name]
    return user_movie_df.corrwith (movie).sort_values(ascending=False).head(head)

movies_from_item_based = item_based_recommender(movie[movie["movieId"] == movie_id]["title"].values[0], user_movie_df, 20).reset_index()
movies_from_item_based.head()
movies_from_item_based.rename(columns={0:"corr"}, inplace=True)
movies_from_item_based.head()

recommended_item_based_df = movies_from_item_based.loc[~movies_from_item_based["title"].isin(movies_watched)][:5]

#Setting up the Hybrid Recommendation (User-based Rec+Item-based Rec)
hybrid_rec_df = pd.concat([recommended_user_based_df["title"], recommended_item_based_df["title"]]).reset_index(drop=True)
hybrid_rec_df
recommended_item_based_df

