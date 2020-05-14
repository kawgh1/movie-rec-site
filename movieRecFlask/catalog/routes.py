# MovieRecSite/catalog/routes.py
from movieRecFlask.catalog import main, recommender2
from movieRecFlask.catalog.forms import GetRecsForm
from flask_login import current_user
from movieRecFlask.catalog.models import UserMovies, RecsClicks

from flask import render_template, flash
from flask_login import login_required

# About page
@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

# Data page
@main.route('/data', methods=['GET', 'POST'])
def data():
    return render_template('data.html')

# 'Home' or Main page (Recommender page)
@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def hello():
    form = GetRecsForm()
    rating_list = []

    # if user logged in
    if current_user.is_authenticated:

        user_id = current_user.get_id()

        user_movies = UserMovies.query.filter_by(user_id=user_id).all()

        if form.validate_on_submit():
            movie_name = form.movie_name.data

            results = recommender2.recommender_final(movie_name)
            movie_list = results[0]
            scores_list = results[1]
            #scores_list = recommender1.get_scores(movie_name)

            # comp_score = scores_list[1] because 1 is the first recommendation, 0 is the movie searched for
            comp_score = scores_list[1]

            movie_id = recommender2.get_movie_id(movie_name)



            # Get Recs clicks are recorded in RecsClicks Table in postgres

            RecsClicks.record_getrecs(
                user_id=user_id,
                movie_id=movie_id,
                movie=movie_name,
                comp_score=comp_score
            )

            for movie in movie_list:
                rating_list.append(recommender2.get_movie_avg(movie))

            # if user logged in and requests recommendation
            return render_template('movies2.html',  movies=movie_list, scores_list=scores_list,
                                   ratings=rating_list, user_movies=user_movies, form=form)
            # if user logged in and no request
        else:
            return render_template('movies1.html',  user_movies=user_movies, form=form)

    else:
        # user not logged in, just display the basic form and results

        # if user not logged in, user_id = 0
        user_id = 0

        if form.validate_on_submit():
            movie_name = form.movie_name.data

            results = recommender2.recommender_final(movie_name)
            movie_list = results[0]
            scores_list = results[1]
            # scores_list = recommender1.get_scores(movie_name)

            # comp_score = scores_list[1] because 1 is the first recommendation, 0 is the movie searched for
            comp_score = scores_list[1]

            movie_id = recommender2.get_movie_id(movie_name)



            # avg_rating = recommender.get_movie_avg(movie_name)
            #
            # movie_returned_from_df = recommender.get_movie_name(movie_name)

            # Get Recs clicks are recorded in RecsClicks Table in postgres

            RecsClicks.record_getrecs(
                user_id=user_id,
                movie_id=movie_id,
                movie=movie_name,
                comp_score=comp_score
            )

            for movie in movie_list:
                rating_list.append(recommender2.get_movie_avg(movie))

            return render_template('movies2.html', movies=movie_list, scores_list=scores_list,
                                   ratings=rating_list, form=form)

        else:
            # If it's a GET request, we just display the basic page with form
            return render_template('movies1.html', form=form)

# Add movie page
@main.route('/add/movie/<item>', methods=['GET'])
@login_required
def add_movie(item):
    form = GetRecsForm()
    user_id = current_user.get_id()

    user_movies = UserMovies.query.filter_by(user_id=user_id).all()

    UserMovies.add_movie1(user_id=user_id, movie=item)

    flash('Successful')

    return render_template('movie_added.html')

# Remove movie page
@main.route('/remove/movie/<item>', methods=['GET'])
@login_required
def remove_movie(item):
    form = GetRecsForm()
    user_id = current_user.get_id()

    user_movies = UserMovies.query.filter_by(user_id=user_id).all()

    UserMovies.remove_movie1(user_id=user_id, movie=item)

    flash('Successful')

    return render_template('movie_removed.html')


# If page not found
@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# # favicon.ico requests
# @main.route('/favicon.ico')
# def page_not_found(error):
#     return render_template('404.html'), 404
