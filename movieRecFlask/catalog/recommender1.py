# MovieRecSite/catalog/recommender.py
from movieRecFlask.catalog import main, routes

from fuzzywuzzy import process
# FuzzyWuzzy takes a string, such as a movie name 'toy story' and corrects for misspellings
# or similar names, matched to the movies in our database
# example user searches for 'Gojira' FuzzyWuzzy returns 'Godzilla'

import pandas as pd
import numpy as np
# import required packages

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity




# CSR Matrix for Recommender method
from scipy.sparse import csr_matrix

# Nearest Neighbors algo for Recommender method
from sklearn.neighbors import NearestNeighbors

# This recommender uses Feature Analysis of genre and tags by users


# 1. Preparing our data
# Create DataFrames
# df_movies = pd.read_csv('movieRecFlask/catalog/data/movies.csv')
# df_ratings = pd.read_csv('movieRecFlask/catalog/data/ratings.csv')

# For df_movies DataFrame use only 'movieId' and 'title' columns
df_movies = pd.read_csv('movieRecFlask/catalog/data/movies.csv', usecols=['movieId', 'title', 'genres'],
                        dtype={'movieId': 'int32', 'title': 'str', 'genres': 'str'})

# Break apart 'genres' into separate words for Feature Analysis
df_movies['genres'] = df_movies['genres'].str.replace("|", " ", 20)

# print(df_movies.head(10))

# For df_ratings DataFrame use only 'userId' and 'movieId' and 'rating' columns
df_ratings = pd.read_csv('movieRecFlask/catalog/data/ratings.csv', usecols=['userId', 'movieId', 'rating'],
                         dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})


df_tags = pd.read_csv('movieRecFlask/catalog/data/tags.csv', usecols=['userId', 'movieId', 'tag'],
                      dtype={'userId': 'int32', 'movieId': 'int32', 'tag': 'str'})



# Create merged ratings and movies table for get_movie_avg_rating method
movie_data = pd.merge(df_ratings, df_movies, on='movieId')
rating_averages = movie_data.groupby('title')['rating'].mean()
s = pd.Series(rating_averages)

df_avg_movie_ratings = s.to_frame()

# Section for getting recommendations by cosine similarity of
# movie tags and genres


# merge tags and movies dataframes
# outer join tags and movies to keep all movies recommendable
# movies_with_tags= pd.merge(df_tags, df_movies, on=['movieId'], how= 'outer')
# fill columns with NaN values for their appropriate data type
# df[['a', 'b']] = df[['a','b']].fillna(value=0)

movies_with_tags= pd.merge(df_tags, df_movies, on=['movieId'])

movies_with_tags['tag'] = movies_with_tags['tag'].fillna(' ')
movies_with_tags['genres'] = movies_with_tags['genres'].fillna(' ')

movies_with_tags['userId'] = movies_with_tags['userId'].fillna(0)
movies_with_tags['userId'] = movies_with_tags['userId'].apply(np.int32)
# make sure userId column is ints and not floats for the database


# movies_with_tags[['genres']] = movies_with_tags[['genres']].fillna('')


# Selecting features from tags and genres

# features = ['tag', 'genres']
# # Replace all NaN values with a empty string
# for feature in features:
#     movies_with_tags[feature] = movies_with_tags[feature].fillna('')


# Create a function that combine all selected Features

def combine_features(row):
    try:
        return row['tag'] + " " + row['genres']
    except:
        print("Error:", row)


movies_with_tags['combined_features'] = movies_with_tags.apply(combine_features, axis=1)


# Creating Count matrix from this new combined_features column
cv = CountVectorizer()
count_matrix = cv.fit_transform(movies_with_tags['combined_features'])


# # Compute the Cosine Similarity based on Count_Matrix
# cosine_sim = cosine_similarity(count_matrix)
# # print (cosine_sim)

# Compute the Cosine Similarity based on Count_Matrix
cosine_sim = cosine_similarity(count_matrix)
# print (cosine_sim)

# helper function to get the movie title of the index of movies_with_tags
# this index is unique to the table is nothing to do with the title or movieId
def get_title_from_index(index):
    return movies_with_tags[movies_with_tags.index == index]["title"].values[0]


# Return the index of the movie_name in the movies_with_tags table
def recommender_final(movie_name):






    list_of_movie_indexes = []
    cos_sim_list = []

    # This only returns the first index matched to the movie_name input
    # but there are multiple indexes for the same movie in movies_with_tags
    movie_index = process.extractOne(movie_name, movies_with_tags['title'])[2]
    full_movie_name = process.extractOne(movie_name, df_movies['title'])[0]

    # need to make a list of movie_indexes of the movie_name

    #     for index in movies_with_tags[movies_with_tags['title'].str.startswith(full_movie_name)]:

    #         list_of_movie_indexes.append(index)

    #     print(list_of_movie_indexes)

    temp_index_df = movies_with_tags[movies_with_tags['title'].str.startswith(full_movie_name)]

    list_of_movie_indexes = list(temp_index_df.index)
    #     print(list_of_movie_indexes)

    #     print("movie_index in movies_with_tags = ", movie_index)

    # go inside of Cosine_matrix and enumerate it
    # similar movies is list of are the indexes of similar movies inside the movies_with_tags table
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    # print(len(similar_movies))

    # Now we get the sorted list with most similar cosine similarity at top
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

    #     for item in sorted_similar_movies:
    #         print(item)

    # Now we are printing the top 10 similar movies

    movie_list = []

    #     print("The top 5 similar movies to " +full_movie_name+ " are:  ")
    for element in sorted_similar_movies[0:10]:

        # if the item in the sorted_similiar movies has the same index (is the same movie)
        # as the movie user searched for...
        # remove that movie title from the recommended movies out
        # (User should not be recommended the same movie they searched for)
        if element[0] in list_of_movie_indexes:
            sorted_similar_movies.remove(element)

    for element in sorted_similar_movies[0:5]:
        movie = get_title_from_index(element[0])
        movie_list.append(movie)


    # remove duplicates of the same movie recommendations in the output
    non_duplicates = [i for n, i in enumerate(movie_list) if i not in movie_list[:n]]

    # the HTML takes the first movie from the list as "movie selected"
    # So we're adding it back here at the front after operations
    # The 1st recommendation wil still be the first recommendation
    non_duplicates.insert(0, full_movie_name)

    #     print(non_duplicates)

    #     print("movie list is ", movie_list)
    #     print("cos_sim_scores are ", cos_sim_list)
    return non_duplicates


# recommender_final("iron man 2008")



#### Get cosine similarity scores

# Return the index of the movie_name in the movies_with_tags table
def get_scores(movie_name):
    list_of_movie_indexes = []
    cos_sim_list = []

    # This only returns the first index matched to the movie_name input
    # but there are multiple indexes for the same movie in movies_with_tags
    movie_index = process.extractOne(movie_name, movies_with_tags['title'])[2]
    full_movie_name = process.extractOne(movie_name, df_movies['title'])[0]

    # need to make a list of movie_indexes of the movie_name

    #     for index in movies_with_tags[movies_with_tags['title'].str.startswith(full_movie_name)]:

    #         list_of_movie_indexes.append(index)

    #     print(list_of_movie_indexes)

    temp_index_df = movies_with_tags[movies_with_tags['title'].str.startswith(full_movie_name)]

    list_of_movie_indexes = list(temp_index_df.index)
    #     print(list_of_movie_indexes)

    #     print("movie_index in movies_with_tags = ", movie_index)

    # go inside of Cosine_matrix and enumerate it
    # similar movies is list of are the indexes of similar movies inside the movies_with_tags table
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    # print(len(similar_movies))

    # Now we get the sorted list with most similar cosine similarity at top
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

    #     for item in sorted_similar_movies:
    #         print(item)

    # Now we are printing the top 10 similar movies

    movie_list = []

    #     print("The top 5 similar movies to " +full_movie_name+ " are:  ")
    for element in sorted_similar_movies[0:20]:

        # if the item in the sorted_similiar movies has the same index (is the same movie)
        # as the movie user searched for...
        # remove that movie title from the recommended movies out
        # (User should not be recommended the same movie they searched for)
        if element[0] in list_of_movie_indexes:
            sorted_similar_movies.remove(element)

    for element in sorted_similar_movies[0:6]:
        sim_score = element[1]
        # convert score to percentage
        sim_score = sim_score*100
        sim_score = round(sim_score, 2)

        cos_sim_list.append(sim_score)


    return cos_sim_list


# return movie_average that user searched for
def get_movie_avg(movie_name):

    full_movie_name = process.extractOne(movie_name, df_movies['title'])[0]

    movie_avg = df_avg_movie_ratings[df_avg_movie_ratings.index == full_movie_name].values[0][0]

    movie_avg = round(movie_avg, 2)

    # print('movie is ', full_movie_name)

    return movie_avg


# get_movie_avg("xXx")

### Auxillary methods to get movie rating average

def get_movie_id(movie_name):

    index = process.extractOne(movie_name, df_movies['title'])[2]

    movie_id = df_movies['movieId'][index]

    movie_id = int(movie_id)

    return movie_id

############################################