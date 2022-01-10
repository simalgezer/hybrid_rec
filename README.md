# Hybrid Recommendation (User-based + Item-based Recommendations)
Recommending a movie with user-based and item-based recommendations 

How does user-based recommendation work? a user-based recommendation suggests movies to a user by finding similar users’ watched movies.

How does item-based recommendation work? an item-based recommendation is made based on the similarity between items — in this case, movie similarity — calculated using people’s ratings of that item. For example, Sarah rated a movie 5 out of 5. Then item-based recommendation suggests other movies that are exposed to similar rating behavior to Sarah’s rating.


Business Problem:
Make a movie recommendation for the user whose ID is given, using the item-based and user-based recommender methods.
The dataset: It was provided by MovieLens, a movie recommendation service. It contains the rating scores for these movies along with the movies. It contains 2,000,0263 ratings across 27,278 movies. The dataset was created by 138,493 users between 09 January 1995 and 31 March 2015. The dataset was created on October 17, 2016. Users are randomly selected. It is known that all selected users voted for at least 20 movies.

Variables:
movie.csv
1. movieId — Unique movie number. (UniqueID)
2. title — Movie name
rating.csv
1. userid — Unique user number. (UniqueID)
2. movieId — Unique movie number. (UniqueID)
3. rating — The rating given to the movie by the user
4. timestamp — Evaluation date
