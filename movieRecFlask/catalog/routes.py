# MovieRecSite/catalog/routes.py
from movieRecFlask.catalog import main, recommender
from movieRecFlask.catalog.forms import GetRecsForm
from flask_login import current_user
from movieRecFlask.catalog.models import UserMovies

from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/data', methods=['GET', 'POST'])
def data():
    return render_template('data.html')


@main.route('/', methods=['GET', 'POST'])
def hello():
    form = GetRecsForm()

    if current_user.is_authenticated:

        user_id = current_user.get_id()

        user_movies = UserMovies.query.filter_by(user_id=user_id).all()

        if form.validate_on_submit():
            movie_name = form.movie_name.data

            movie_list = recommender.recommender2(movie_name)
            # if user logged in and requests recommendation
            return render_template('movies2.html',  movies=movie_list, user_movies=user_movies, form=form)
            # if user logged in and no request
        else:
            return render_template('movies1.html',  user_movies=user_movies, form=form)

    else:
        # user not logged in, just display the basic form and results
        if form.validate_on_submit():
            movie_name = form.movie_name.data

            movie_list = recommender.recommender2(movie_name)

            return render_template('movies2.html', movies=movie_list, form=form)

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
