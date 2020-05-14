# MovieRecSite/catalog/recommender2.py



# These sklearn are for keyword recommender feature analysis
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity





import pandas as pd
import numpy as np

# CSR Matrix for KNN Recommender method
from scipy.sparse import csr_matrix

# Nearest Neighbors algo for KNN Recommender method
from sklearn.neighbors import NearestNeighbors

from fuzzywuzzy import process
# FuzzyWuzzy takes a string, such as a movie name 'toy story' and corrects for misspellings
# or similar names, matched to the movies in our database
# example user searches for 'Gojira' FuzzyWuzzy returns 'Godzilla'



# Preparing the Data
######################

# 1. Preparing our data
# Create DataFrames

# For df_movies DataFrame use only 'movieId' and 'title' columns
df_movies = pd.read_csv('movieRecFlask/catalog/data/movies.csv', usecols=['movieId', 'title', 'genres'],
                        dtype={'movieId': 'int32', 'title': 'str', 'genres': 'str'})

# Break apart 'genres' into separate words for Feature Analysis
df_movies['genres'] = df_movies['genres'].str.replace("|", " ", 20)

# For df_ratings DataFrame use only 'userId' and 'movieId' and 'rating' columns
df_ratings = pd.read_csv('movieRecFlask/catalog/data/ratings.csv', usecols=['userId', 'movieId', 'rating'],
                         dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

# Removing the 'timestamp' and 'userId' columns from df_tags
# because we aren't using them in the recommender
df_tags = pd.read_csv('movieRecFlask/catalog/data/tags.csv', usecols=['movieId', 'tag'],
                      dtype={'movieId': 'int32', 'tag': 'str'})



# Create merged ratings and movies table for get_movie_avg_rating method
movie_data = pd.merge(df_ratings, df_movies, on='movieId')
rating_averages = movie_data.groupby('title')['rating'].mean()
s = pd.Series(rating_averages)

df_avg_movie_ratings = s.to_frame()




# THIS FILE CONTAINS 2 SEPARATE RECOMMENDATION ENGINES
# AND IS DIVIDED INTO 3 SECTIONS

###########################################################
# Section 1 - Keyword Recommender Set up
# ######### - Most recs will come from here
# ######### - Movies not found in this one use the next one
###########################################################

# this line combines multiple rows of the same movies with different tags
# into a single row of that movie with the various user assigned tags
df_new_tags = df_tags.groupby('movieId').agg(lambda x: ' '.join(x.unique()))

movies_with_tags= pd.merge(df_new_tags, df_movies, on=['movieId'])

# fill columns with NaN values for their appropriate data type
# df[['a', 'b']] = df[['a','b']].fillna(value=0)

movies_with_tags['tag'] = movies_with_tags['tag'].fillna(' ')
movies_with_tags['genres'] = movies_with_tags['genres'].fillna(' ')




# Create a function that combine all selected Features

def combine_features(row):
    try:
        return row['tag'] + " " + row['genres']
    except:
        print("Error:", row)


movies_with_tags['combined_features'] = movies_with_tags.apply(combine_features, axis=1)


del movies_with_tags['tag']
del movies_with_tags['genres']


# Creating Count matrix from this new combined_features column
cv = CountVectorizer()
count_matrix = cv.fit_transform(movies_with_tags['combined_features'])

# Compute the Cosine Similarity based on Count_Matrix
cosine_sim = cosine_similarity(count_matrix)
##########################################################
# End section 1 for Keyword recommedner
##########################################################






###########################################################
# Section 2 - Nearest Neighbor Recommender Set up
# ######### - All other recs will come from here
###########################################################

movie_features_df = df_ratings.pivot_table(index='movieId', columns = 'userId', values='rating').fillna(0)


# Create Compressed Sparse Row (CSR) Matrix
mat_movies_users = csr_matrix(movie_features_df.values)

# Create algo model for recommender
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6)
# Fit model using CSR matrix
model_knn.fit(mat_movies_users)
##########################################################
# End section 2 for Nearest Neighbor recommedner
##########################################################


#############################################################################
#############################################################################
# Section 3 - The Recommender Engine and methods that use both Sections above
#############################################################################
#############################################################################


# helper function to get the movie title of the index of movies_with_tags
# this index is unique to the table is nothing to do with the title or movieId
def get_title_from_index(index):
    return movies_with_tags[movies_with_tags.index==index]["title"].values[0]

# Return the index of the movie_name in the movies_with_tags table
def recommender_final(movie_name):
    movie_list = []
    cos_sim_list = []

    #     movie_index = process.extractOne(movie_name, df_movies['title'])[2]

    full_movie_name = process.extractOne(movie_name, df_movies['title'])[0]

    # If movie index in movies_with_tags - do keyword recommendation
    if (movies_with_tags['title'] == full_movie_name).any():

        movie_index = process.extractOne(movie_name, movies_with_tags['title'])[2]

        # print(True)

        #     keyword_movie_index = process.extractOne(movie_name, movies_with_tags['title'])[2]
        #     keyword_full_movie_name = process.extractOne(movie_name, movies_with_tags['title'])[0]
        #     universe_movie_index = process.extractOne(movie_name, df_movies['title'])[2]
        #     universe_full_movie_name = process.extractOne(movie_name, df_movies['title'])[0]

        # go inside of Cosine_matrix and enumerate it
        # similar movies is list of are the indexes of similar movies inside the movies_with_tags table
        similar_movies = list(enumerate(cosine_sim[movie_index]))

        # Now we get the sorted list with most similar cosine similarity at top
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        # Return the first 6 movies in sort_similar_movies
        for element in sorted_similar_movies[0:6]:
            movie = get_title_from_index(element[0])
            movie_list.append(movie)
            sim_score = element[1]
            # convert score to percentage
            sim_score = sim_score * 100
            sim_score = round(sim_score, 2)
            cos_sim_list.append(sim_score)

        # the HTML takes the first movie from the list as "movie selected"
        # So we're adding it back here at the front after operations
        # The 1st recommendation will still be the first recommendation
        #movie_list.insert(0, full_movie_name)

        #         print('keyword_movie_index =', keyword_movie_index, '\n'
        #         'keyword_full_movie_name =', keyword_full_movie_name, '\n'
        #         'universe_movie_index =', universe_movie_index, '\n'
        #         'universe_full_movie_name =', universe_full_movie_name, '\n')

        results = [movie_list, cos_sim_list]
        return results

    # IF user searched movie NOT in our keyword table of movies
    # Then do a recommendation based on user ratings which is less accurate,
    # but has a larger universe of movies to get recommendations for
    else:

        movie_index = process.extractOne(movie_name, df_movies['title'])[2]

        distances, indices = model_knn.kneighbors(mat_movies_users[movie_index])

        # print('distances, indices = ', distances, indices)

        # print(indices[0][1])

        movie_rec_list = []
        distance_list = []

        for i in indices[0]:
            movie = (df_movies['title'][i])
            movie_rec_list.append(movie)

        # We only want the 5 scores returned
        for j in distances[0]:
            j = j * 100
            score = round(100 - j, 2)

            distance_list.append(score)

        results = [movie_rec_list, distance_list]
        return results

# recommender_final("101 dalmations")



################################################################
# ## Auxillary methods to get movie rating average and movie id
################################################################

def get_movie_id(movie_name):

    index = process.extractOne(movie_name, df_movies['title'])[2]

    movie_id = df_movies['movieId'][index]

    movie_id = int(movie_id)

    return movie_id

# return movie_average that user searched for
def get_movie_avg(movie_name):

    full_movie_name = process.extractOne(movie_name, df_movies['title'])[0]
    # Not all movies had ratings
    if full_movie_name in df_avg_movie_ratings.index:

        movie_avg = df_avg_movie_ratings[df_avg_movie_ratings.index == full_movie_name].values[0][0]

        movie_avg = round(movie_avg, 2)

        # print('movie is ', full_movie_name)

        return movie_avg

    else:
        return 'None'


# get_movie_avg("toy story")

# ###########################################

