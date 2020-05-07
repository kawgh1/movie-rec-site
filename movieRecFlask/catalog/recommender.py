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


### Auxillary methods to get movie rating average

def get_movie_id(movie_name):

    index = process.extractOne(movie_name, df_movies['title'])[2]

    movie_id = df_movies['movieId'][index]

    movie_id = int(movie_id)

    return movie_id

def get_movie_name(movie_name):

    index = process.extractOne(movie_name, df_movies['title'])[2]

    name_found_in_df = df_movies['title'][index]

    return name_found_in_df

def get_movie_avg(movie_name):
    index = process.extractOne(movie_name, df_movies['title'])[2]
    # print("Movie Selected:  ", df_movies['title'][index], 'Index:  ', index)
    # print("getting avg....")

    movie_id = df_movies['movieId'][index]

    # print('Movie ID ', movie_id, 'Index: ', index)

    # df.loc[df['column_name'] == some_value]

    # ratings = all the rows of df_rating where movieId == movie_id of movie searched for
    ratings = df_ratings.loc[df_ratings['movieId'] == movie_id]
    # ratings_sum = sum of all the numerical ratings for our movie
    ratings_sum = ratings['rating'].sum()
    # count = how many rows are in ratings
    count = len(ratings.index)

    average_rating = (ratings_sum) / count

    final_avg = round(average_rating, 2)

    #     print(df_ratings.loc[df_ratings['movieId'] == movie_id])
    #     print('Count = ', count)
    #     print('ratings sum = ', ratings_sum)
    #     print('average rating = ', final_avg)

    # executive decision - if a movie has less than 2 ratings
    # return the average movie rating to equal '3' due to lack of
    # a meaningful average
    # I don't want a movie with 1 review of '5' next to a movie with 100 reviews at '4.25'

    # if count < 2:
    #     final_avg = 3.0

    return final_avg

##############################################################


def recommender_final(movie_name):
    index = process.extractOne(movie_name, df_movies['title'])[2]
    # print("Movie Selected:  ", df_movies['title'][index], 'Index:  ', index)
    # print("Searching for recommendations....")

    distances, indices = model_knn.kneighbors(mat_movies_users[index])

    # print('distances, indices = ', distances, indices)

    # print(indices[0][1])

    movie_rec_list = []
    distance_list = []

    # How to include the average movie rating as part of the movie title returned

    # for i in indices[0]:
    #     movie = (df_movies['title'][i])
    #     movie_rating = get_movie_avg(movie)
    #     # if movie_rating is not None:
    #     movie = movie + ' - ' + str(movie_rating)
    #     movie_rec_list.append(movie)

    for i in indices[0]:
        movie = (df_movies['title'][i])
        movie_rec_list.append(movie)

    # for i in movie_rec_list[1:]:
    #     print(i)

    # print(movie_rec_list[1:])
    return movie_rec_list

#############

