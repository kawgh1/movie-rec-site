# MovieRecSite/catalog/recommender.py
from movieRecFlask.catalog import main, routes

from fuzzywuzzy import process
# FuzzyWuzzy takes a string, such as a movie name 'toy story' and corrects for misspellings
# or similar names, matched to the movies in our database
# example user searches for 'Gojira' FuzzyWuzzy returns 'Godzilla'

import pandas as pd


# CSR Matrix for Recommender method
from scipy.sparse import csr_matrix

# Nearest Neighbors algo for Recommender method
from sklearn.neighbors import NearestNeighbors

# 1. Preparing our data
# Create DataFrames
df_movies = pd.read_csv('movieRecFlask/catalog/data/movies.csv')
df_ratings = pd.read_csv('movieRecFlask/catalog/data/ratings.csv')

# For df_movies DataFrame use only 'movieId' and 'title' columns
df_movies = pd.read_csv('movieRecFlask/catalog/data/movies.csv', usecols=['movieId', 'title'],
                        dtype={'movieId': 'int32', 'title': 'str'})
# print(df_movies.head(10))

# For df_ratings DataFrame use only 'userId' and 'movieId' and 'rating' columns
df_ratings = pd.read_csv('movieRecFlask/catalog/data/ratings.csv', usecols=['userId', 'movieId', 'rating'],
                         dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

# print(df_ratings.head(10))

# Merge df_movies and df_ratings into df_merge on 'movieId' column
df_merge = pd.merge(df_ratings, df_movies, on='movieId')
# print(df_merge.head(10))

# Any reason to install matplotlib?
# print(df_merge.rating.plot.hist())

# Create a pivot table of df_merge
df_merge = df_merge.pivot(index='movieId', columns = 'userId', values = 'rating')

# Fill NaN values with 0s to make a CSR Matrix
df_merge = df_merge.fillna(0)

# Create Compressed Sparse Row (CSR) Matrix
mat_movies_users = csr_matrix(df_merge.values)

# Create algo model for recommender
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6)
# Fit model using CSR matrix
model_knn.fit(mat_movies_users)

# For Tuning/Testing/Dev Use
#
# Recommender_Plus function
# Recommender_Plus takes a movie name and returns a list of movies recommended to us
# Along with their cosine differences
# A smaller cosine value indicates a 'better' or 'closer' recommenderation to the
# movie input


def recommender_plus(movie_name, data, model, n_recommendations):
    model.fit(data)
    index = process.extractOne(movie_name, df_movies['title'])[2]
    print("Movie Selected:  ", df_movies['title'][index], 'Index:  ', index)
    print("Searching for recommendations....")

    distances, indices = model.kneighbors(data[index], n_neighbors=n_recommendations)

    # print('distances, indices = ', distances, indices)

    # print(indices[0][1])

    movie_rec_list = []
    distance_list = []

    for i in indices[0]:
        if i == 0:
            i = i + 1
        else:
            # print(df_movies['title'][i])
            movie = (df_movies['title'][i])
            movie_rec_list.append(movie)

        # print('--------------------------------------')

    # print('\n\n\n')

    # for i in indices[0]:
        # print(df_movies['title'][i])
        # print('--------------------------------------')

    # print('\n\n\n')

    for j in range(0, len(distances.flatten())):
        if j == 0:
            j = j + 1
        else:
            # print(', with distance of {0}:'.format(   distances.flatten()[j]))
            distance = ('with distance of {0}:'.format(distances.flatten()[j]))
            distance_list.append(distance)

    #  z = list(zip(x,y))

    # the list(zip(list1,list2)) method takes two lists and creates a list of tuples for each pair in list1 and list2

    movie_and_distance_list_of_tuples = list(zip(movie_rec_list, distance_list))

    for i in movie_and_distance_list_of_tuples[1:]:
        print(i)


# recommender_plus('jurassic park', mat_movies_users, model_knn, 6)


def recommender2(movie_name):
    index = process.extractOne(movie_name, df_movies['title'])[2]
    # print("Movie Selected:  ", df_movies['title'][index], 'Index:  ', index)
    # print("Searching for recommendations....")

    distances, indices = model_knn.kneighbors(mat_movies_users[index])

    # print('distances, indices = ', distances, indices)

    # print(indices[0][1])

    movie_rec_list = []
    distance_list = []

    for i in indices[0]:
        movie = (df_movies['title'][i])
        movie_rec_list.append(movie)

    # for i in movie_rec_list[1:]:
    #     print(i)

    # print(movie_rec_list[1:])
    return movie_rec_list


# recommender2('diehard')