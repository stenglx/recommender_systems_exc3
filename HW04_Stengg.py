import pandas as pd
import numpy as np


def createUserProfile():
    # 1) Create a user profile based on the genres of the movies.
    # Count how often each movie genre appeared in the set of the movies
    # that the user has liked (i.e., when the rating is greater than 3).

    # drop if rating is 3 or worse
    user_ratings_filtered = user_ratings.loc[user_ratings['rating'] > 3]

    # get genres from being genre1|genre2|... into seperated rows with duplicated other values
    user_ratings_filtered_split = user_ratings_filtered
    user_ratings_filtered_split['genres'] = user_ratings_filtered['genres'].str.split("|")
    #print(user_ratings_filtered_split.to_string())
    user_ratings_filtered_split = user_ratings_filtered_split.explode('genres')
    #print(user_ratings_filtered_split.to_string())

    # count ratings per genres
    counted_ratings_per_genre = user_ratings_filtered_split.groupby('genres')['genres'].count()
    #print(counted_ratings_per_genre)
    return counted_ratings_per_genre


def getSimilarities():
    # 2) Determine the similarity of each recommendable movie to this user profile.
    # Implement a simple strategy that simply determines the overlap in genres, ignoring how many movies of a certain genre the user has liked.
    # Inspect the outcomes of this recommendation strategy for a few users.
    similarities_ids = set() # such that no movie is recommended more than once
    similarities_ids_dict = {}  # such that no movie is recommended more than once (key is id)
    #print('Trying to get similarities for {}'.format(user_id))
    #liked_genres = set(user_profile.to_dict().keys())
    #print(liked_genres)

   # movies_ = data
   # movies_['genres'] = movies_['genres'].str.split("|")
   # print(movies_.to_string())
    for index, movie in data.iterrows():
      #  print(movie)
        if movie['user_id'] == user_id:
            continue
        genres =  movie['genres'].split("|")
       # print(genres)
        #print(liked_genres)
       # break
        intersected_set = set(genres).intersection(liked_genres)
        #print(index, '***',intersected_set)
        if intersected_set:
            #print(intersected_set)
            #print(len(intersected_set))
            # if intersection of genres -> add to similar movies which are up for reccomendation
            #sim.append(movie) # append is deprecated
            similarities_ids.add(movie['movie_id'])
            similarities_ids_dict[movie['movie_id']] =  len(intersected_set)
          #  print(len(intersected_set))
        #else:
           # print(len(intersected_set))
            #print('no overlap')

    #sim2 = pd.DataFrame(similarities,
     #            columns=['user_id', 'movie_id', 'rating', 'timestamp', 'gender', 'age', 'occupation', 'zip', 'title',
      #                    'genres'])
    #similarities = pd.DataFrame.from_records(sim)
    #sim2 = sim.groupby('movie_id')
    # we now have movie id's of all recommended movies
    similarities_ids_list = list(similarities_ids) # bc set is not spscribtable
    similarities_ids_list.sort(reverse=True)
    #similarities_ids_list = list(similarities_ids_dict)  # bc set is not spscribtable
    sorted_dict_similarities = dict(sorted(similarities_ids_dict.items(), key=lambda x: x[1], reverse=True)[:10])
    #sorted_dict_similarities = dict(sorted(similarities_ids_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
    #print(sorted_dict_similarities)
    #print(sorted_dict_similarities.keys())
    keys = sorted_dict_similarities.keys()
    return list(keys)

    return similarities_ids_list[:10]


def getSimilaritiesExtended():
    # 3) Extend the algorithm as follows. When recommending, remove all movies that have no overlap with the given user profile.
    # Rank the remaining items based on their popularity1. Again, test your method with a few users.
    # 1 You can determine the popularity of any item by counting the numbers of ratings for it.
    similarities_ids = set() # such that no movie is recommended more than once
    similarities_ids_dict = {}  # such that no movie is recommended more than once (key is id)
    #print('Trying to get similarities for {}'.format(user_id))

    #print(liked_genres)

   # movies_ = data
   # movies_['genres'] = movies_['genres'].str.split("|")
   # print(movies_.to_string())
    for index, movie in data.iterrows():
      #  print(movie)
        if movie['user_id'] == user_id:
            continue
        genres =  movie['genres'].split("|")
       # print(genres)
        #print(liked_genres)
       # break
        intersected_set = set(genres).intersection(liked_genres)
        #print(index, '***',intersected_set)
        # skip ones with no overlap
        if intersected_set:
            #print(intersected_set)
            #print(len(intersected_set))
            # if intersection of genres -> add to similar movies which are up for reccomendation
            #sim.append(movie) # append is deprecated
            similarities_ids.add(movie['movie_id'])
            #similarities_ids_dict[movie['movie_id']] =  len(intersected_set)
       # else:
        #    print(len(intersected_set))
         #   print('no overlap')

    #sim2 = pd.DataFrame(similarities,
     #            columns=['user_id', 'movie_id', 'rating', 'timestamp', 'gender', 'age', 'occupation', 'zip', 'title',
      #                    'genres'])
    #similarities = pd.DataFrame.from_records(sim)
    #sim2 = sim.groupby('movie_id')

    # 1 You can determine the popularity of any item by counting the numbers of ratings for it.
    #for movie in sim_movie_ids:+

    #print('IDs',similarities_ids)

    possible_movies = data[data['movie_id'].isin(list(similarities_ids))]
    #print(possible_movies)

    counted_ratings_per_genre = possible_movies.groupby('movie_id')['rating'].mean()
    #print('avergae rating per movie')
    #print(counted_ratings_per_genre.to_string())

    sorted_dict_ratings = dict(sorted(counted_ratings_per_genre.items(), key=lambda x: x[1], reverse=True)[:10])
    #print (sorted_dict_ratings)
    # {989: 5.0, 1830: 5.0, 3172: 5.0, 3233: 5.0, 3280: 5.0, 3382: 5.0, 3607: 5.0, 3656: 5.0, 3245: 4.8, 53: 4.75}
    # tested with user 123
    # none of the recommended movies regarding rating and overlap were rated already by the user so shall be fine
    return sorted_dict_ratings

def getSimilaritiesExtendedGenreCount():
    # 4) Implement a method that also considers the “genre‐count” in the user profile in some form.
    similarities_ids = set() # such that no movie is recommended more than once
    similarities_ids_dict = {}  # such that no movie is recommended more than once (key is id)
    #print('Trying to get similarities for {}'.format(user_id))

    #print(liked_genres)

   # movies_ = data
   # movies_['genres'] = movies_['genres'].str.split("|")
   # print(movies_.to_string())
    for index, movie in data.iterrows():
      #  print(movie)
        if movie['user_id'] == user_id:
            continue
        genres =  movie['genres'].split("|")
       # print(genres)
        #print(liked_genres)
       # break
        intersected_set = set(genres).intersection(liked_genres)
        #print(index, '***',intersected_set)
        # skip ones with no overlap
        if intersected_set:
            #print(intersected_set)
            #print(len(intersected_set))
            # if intersection of genres -> add to similar movies which are up for reccomendation
            #sim.append(movie) # append is deprecated
            similarities_ids.add(movie['movie_id'])
            #similarities_ids_dict[movie['movie_id']] =  len(intersected_set)
       # else:
        #    print(len(intersected_set))
         #   print('no overlap')

    #sim2 = pd.DataFrame(similarities,
     #            columns=['user_id', 'movie_id', 'rating', 'timestamp', 'gender', 'age', 'occupation', 'zip', 'title',
      #                    'genres'])
    #similarities = pd.DataFrame.from_records(sim)
    #sim2 = sim.groupby('movie_id')

    # 1 You can determine the popularity of any item by counting the numbers of ratings for it.
    #for movie in sim_movie_ids:+

    #print('IDs',similarities_ids)

    possible_movies = data[data['movie_id'].isin(list(similarities_ids))]
    #print(possible_movies)

    counted_ratings_per_genre = possible_movies.groupby('movie_id')['rating'].mean()
    #print('avergae rating per movie')
    #print(counted_ratings_per_genre.to_string())

    sorted_dict_ratings = dict(sorted(counted_ratings_per_genre.items(), key=lambda x: x[1], reverse=True)[:10])
    #print (sorted_dict_ratings)
    # {989: 5.0, 1830: 5.0, 3172: 5.0, 3233: 5.0, 3280: 5.0, 3382: 5.0, 3607: 5.0, 3656: 5.0, 3245: 4.8, 53: 4.75}
    # tested with user 123
    # none of the recommended movies regarding rating and overlap were rated already by the user so shall be fine
    return sorted_dict_ratings




if __name__ == '__main__':
    print('Running the popularity‐aware content‐based recommender')

    # A) Accepts the user ID as input (on the console)
    user_id = input("Enter user ID: ")
    try:
        user_id = int(user_id)
    except ValueError:
        print("Error: user ID must be an integer")
        exit()

    # Load the MovieLens dataset
    ratings = pd.read_csv('./ratings.dat', sep='::', engine='python', names=[
        'user_id', 'movie_id', 'rating', 'timestamp'])
    movies = pd.read_csv('./movies.dat', sep='::', engine='python', names=[
        'movie_id', 'title', 'genres'], encoding='ISO-8859-1')
    users = pd.read_csv('./users.dat', sep='::', engine='python', names=[
        'user_id', 'gender', 'age', 'occupation', 'zip'], encoding='ISO-8859-1')


    # B) Displays the user profile in terms of the rated items
    # Merge the data
    data = pd.merge(ratings, users, on='user_id')
    data = pd.merge(data, movies, on='movie_id')
    print(data)

    print('User profile in terms of rated items of the user:')
    #print(data[data['user_id'] == user_id].to_string(
     #   index=False))
    user_ratings = data[data['user_id'] == user_id]
    #print(user_ratings.to_string(
     #   index=False))

    # C) Prints the top‐10 recommendations on the console. To implement the algorithm:

    # 1) Create a user profile based on the genres of the movies.
    # Count how often each movie genre appeared in the set of the movies
    # that the user has liked (i.e., when the rating is greater than 3).
    user_profile = createUserProfile()

    # for futher use in the similarity methods I want the genres liked by the user as set
    liked_genres = set(user_profile.to_dict().keys())

    # 2) Determine the similarity of each recommendable movie to this user profile.
    # Implement a simple strategy that simply determines the overlap in genres, ignoring how many movies of a certain genre the user has liked.
    # Inspect the outcomes of this recommendation strategy for a few users.
    sim_movie_ids = getSimilarities()
    print('Recommended movies according to C2) (overlap in genres)')
    print (movies[movies['movie_id'].isin(sim_movie_ids)].to_string())

    # 3) Extend the algorithm as follows. When recommending, remove all movies that have no overlap with the given user profile.
    # Rank the remaining items based on their popularity1. Again, test your method with a few users.
    # 1 You can determine the popularity of any item by counting the numbers of ratings for it.
    sim_movie_ids_extended = getSimilaritiesExtended()
    print('Recommended movies according to C3) (overlap in genres extended)')
    print (movies[movies['movie_id'].isin(sim_movie_ids_extended)].to_string())

    # 4) Implement a method that also considers the “genre‐count” in the user profile in some form.
    sim_movie_ids_extended_genre_count = getSimilaritiesExtendedGenreCount()
    print('Recommended movies according to C3) (overlap in genres extended)')
    print (movies[movies['movie_id'].isin(sim_movie_ids_extended_genre_count)].to_string())

    # Test your method interactively with a few users to check the plausibility of the recommendations.
    # Use the MovieLens1M dataset for testing your program. Structure your program code in functions and/or classes.
    # Implement appropriate error handling procedures.