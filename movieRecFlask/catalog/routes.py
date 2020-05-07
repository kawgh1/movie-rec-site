# MovieRecSite/catalog/routes.py
from movieRecFlask.catalog import main, recommender
from movieRecFlask.catalog.forms import GetRecsForm
from flask_login import current_user
from movieRecFlask.catalog.models import UserMovies, RecsClicks

from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required

# for dashboard visualization data
from movieRecFlask.plotlydash import dashdata, dashboard
import csv
from datetime import datetime
from datetime import date




@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/data', methods=['GET', 'POST'])
def data():
    return render_template('data.html')


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def hello():
    form = GetRecsForm()
    rating_list = []

    # if user logged in
    if current_user.is_authenticated:

        user_id = current_user.get_id()

        user_movies = UserMovies.query.filter_by(user_id=user_id).all()

        if form.validate_on_submit():
            movie_name = form.movie_name.data

            movie_list = recommender.recommender_final(movie_name)

            movie_id = recommender.get_movie_id(movie_name)

            # avg_rating = recommender.get_movie_avg(movie_name)
            #
            # movie_returned_from_df = recommender.get_movie_name(movie_name)

            # Get Recs clicks are recorded in RecsClicks Table in postgres

            RecsClicks.record_getrecs(
                user_id=user_id,
                movie_id=movie_id,
                movie=movie_name
            )

            # This commented section is deprecated
            #
            # # plotlydash/dashdata/recs-click.csv section
            # # header = ['date', 'userId', 'movieId', 'titleSearched', 'titleReturned', 'avg-rating']
            # # User ID == 0 is used for anonymous, not logged in users
            # row = [date.today(), user_id, movie_id, movie_name, movie_returned_from_df, avg_rating]
            #
            # with open('movieRecFlask/plotlydash/dashdata/recs-clicked.csv', 'a', newline='', encoding='utf-8') as f:
            #     csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #     # csv_writer.writerow(header)
            #     csv_writer.writerow(row)

            for movie in movie_list:
                rating_list.append(recommender.get_movie_avg(movie))

            # if user logged in and requests recommendation
            return render_template('movies2.html',  movies=movie_list, ratings=rating_list, user_movies=user_movies, form=form)
            # if user logged in and no request
        else:
            return render_template('movies1.html',  user_movies=user_movies, form=form)

    else:
        # user not logged in, just display the basic form and results

        # if user not logged in, user_id = 0
        user_id = 0

        if form.validate_on_submit():
            movie_name = form.movie_name.data

            movie_list = recommender.recommender_final(movie_name)

            movie_id = recommender.get_movie_id(movie_name)

            # avg_rating = recommender.get_movie_avg(movie_name)
            #
            # movie_returned_from_df = recommender.get_movie_name(movie_name)

            # Get Recs clicks are recorded in RecsClicks Table in postgres

            RecsClicks.record_getrecs(
                user_id=user_id,
                movie_id=movie_id,
                movie=movie_name
            )

            # This commented section is deprecated
            #
            # # plotlydash/dashdata/recs-click.csv section
            # header = ['date', 'userId', 'movieId', 'titleSearched', 'titleReturned', 'avg-rating']
            # # User ID == 0 is used for anonymous, not logged in users
            # row = [date.today(), 0, movie_id, movie_name, movie_returned_from_df, avg_rating]
            #
            # with open('movieRecFlask/plotlydash/dashdata/recs-clicked.csv', 'a', newline='', encoding='utf-8') as f:
            #     csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #     # csv_writer.writerow(header)
            #     csv_writer.writerow(row)

            for movie in movie_list:
                rating_list.append(recommender.get_movie_avg(movie))

            return render_template('movies2.html', movies=movie_list, ratings=rating_list, form=form)

        else:
            # If it's a GET request, we just display the basic page with form
            return render_template('movies1.html', form=form)


@main.route('/add/movie/<item>', methods=['GET'])
@login_required
def add_movie(item):
    form = GetRecsForm()
    user_id = current_user.get_id()

    user_movies = UserMovies.query.filter_by(user_id=user_id).all()

    UserMovies.add_movie1(user_id=user_id, movie=item)

    flash('Successful')

    return render_template('movie_added.html')


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
