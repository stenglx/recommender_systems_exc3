# coding=utf-8
import pandas as pd

# 1) Create a user profile based on the genres of the movies.
# Count how often each movie genre appeared in the set of the movies
# that the user has liked (i.e., when the rating is greater than 3).
def createUserProfile():
    # drop if rating is 3 or worse
    user_ratings_liked = user_ratings[user_ratings['rating'] > 3]

    user_genre = movies[movies['movie_id'].isin(user_ratings_liked['movie_id'])][
        'genres'].str.get_dummies(sep='|').sum() # Genre1|Genre2|...|GenreX needs to be split up

    print('\nGenres rated by user {}:'.format(user_id))
    print(user_genre.index.to_list)
    print('\nLiked movies per genre: \n'.format(user_id))
    print(user_genre)
    # generate ratings data frame of user, which contains all genres
    user_genre = pd.DataFrame(user_genre).T
    user_genre = user_genre.merge(genre_matrix, how='left')
    user_genre = user_genre.reindex(sorted(user_genre.columns),
                                    axis=1)
    return user_genre

# 2) Determine the similarity of each recommendable movie to this user profile.
# Implement a simple strategy that simply determines the overlap in genres, ignoring how many movies of a certain genre the user has liked.
# Inspect the outcomes of this recommendation strategy for a few users.
def getSimilarities_ContentBased(user_genre):
    # ignoring how many movies of a certain genre the user has liked
    user_genre[~user_genre.isnull()] = 1
    user_genre = user_genre.fillna(0) # not liked movies get a 0 instead of null
    similarity = genre_matrix.dot(user_genre.T)
    similarity = similarity.sort_values(by=0, ascending=False)
    # recommend 10 movies with most overlapping
    movies_recommended = movies[movies.index.isin(similarity[:10].index)]
    print('\nTop 10 recommended Movies for user {}:'.format(user_id))
    print(movies_recommended[['title', 'genres']].to_string(index=False))
    print('\n')
    return similarity

# 3) Extend the algorithm as follows. When recommending, remove all movies that have no overlap with the given user profile.
# Rank the remaining items based on their popularity1. Again, test your method with a few users.
# 1 You can determine the popularity of any item by counting the numbers of ratings for it.
def getSimilarities_PopularityBased(similarity):
    # remove all movies that have no overlap with the given user profile
    similarity = similarity[similarity[0] != 0]
    ratings_recommended_movie = ratings[ratings['movie_id'].isin(
        similarity.index)]
    rating_count = ratings_recommended_movie['movie_id'].value_counts()
    # Rank the remaining items based on their popularity
    rating_count = rating_count.sort_values(ascending=False)
    # recommend 10 popular movie
    movies_recommended = movies[movies['movie_id'].isin(rating_count[:10].index)][
        ['title', 'genres']]
    print('Top 10 popular movies for user {}:'.format(user_id))
    print(movies_recommended.to_string(index=False))
    print('\n')

# 4) Implement a method that also considers the “genre‐count” in the user profile in some form.
def getSimilarities_ContentBased_Extended(user_genre):
    # normalization to get amount of all genres into account, rest is as C2 but we don't set the count of the genres to 1
    user_genre = user_genre.fillna(0)
    similarity = genre_matrix.dot(user_genre.T)/user_genre.sum() # normalization
    similarity = similarity.sort_values(by=0, ascending=False)
    # recommend 10 movies with most overlapping
    movies_recommended = movies[movies.index.isin(similarity[:10].index)]
    print('Top 10 recommended Movies for user {}:'.format(user_id))
    print(movies_recommended[['title', 'genres']].to_string(index=False))
    print('\n')

if __name__ == '__main__':
    print('Starting the popularity‐aware content‐based Recommender')

############# A) Accepts the user ID as input (on the console)
    user_id = input("Enter user ID: ")
    try:
        user_id = int(user_id)
    except ValueError:
        print("Error: user ID must be an integer")
        exit()

    # Load the MovieLens dataset files ratings and movies
    ratings = pd.read_csv('ratings.dat', sep='::', engine='python', names=[
        'user_id', 'movie_id', 'rating', 'timestamp'])
    movies = pd.read_csv('movies.dat', sep='::', engine='python', names=[
        'movie_id', 'title', 'genres'], encoding='ISO-8859-1')

############# B) Displays the user profile in terms of the rated items
    print('Top 10 movies rated by the user:')
    user_ratings = ratings[ratings['user_id'] == user_id]
    user_ratings.sort_values(by='rating', ascending=False)
    if len(user_ratings):
        print(movies[movies['movie_id'].isin(user_ratings['movie_id'])][[
                               'title','genres']][:10].to_string())
    else:
        print('User rated no movies! Exit')
        exit()

    # Create a DataFrame containing the genres of each movie exclude the
    # movies user have watched
    genre_matrix = movies[~movies['movie_id'].isin(user_ratings['movie_id'])]['genres'].str.get_dummies(sep='|')

############# C) Prints the top‐10 recommendations on the console.

# 1) Create a user profile based on the genres of the movies.
    # Count how often each movie genre appeared in the set of the movies
    # that the user has liked (i.e., when the rating is greater than 3).
    matrix_user_genres = createUserProfile()

# 2) Determine the similarity of each recommendable movie to this user profile.
    # Implement a simple strategy that simply determines the overlap in genres, ignoring how many movies of a certain genre the user has liked.
    # Inspect the outcomes of this recommendation strategy for a few users.
    similarities = getSimilarities_ContentBased(matrix_user_genres)

# 3) Extend the algorithm as follows. When recommending, remove all movies that have no overlap with the given user profile.
    # Rank the remaining items based on their popularity1. Again, test your method with a few users.
    # 1 You can determine the popularity of any item by counting the numbers of ratings for it.
    getSimilarities_PopularityBased(similarities)

# 4) Implement a method that also considers the “genre‐count” in the user profile in some form.
    getSimilarities_ContentBased_Extended(matrix_user_genres)

    # Test your method interactively with a few users to check the plausibility of the recommendations.
    # Use the MovieLens1M dataset for testing your program. Structure your program code in functions and/or classes.
    # Implement appropriate error handling procedures.