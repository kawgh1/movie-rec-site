from movieRecFlask.catalog import main, recommender
from movieRecFlask.catalog.forms import GetRecsForm
from flask_login import current_user
from movieRecFlask.catalog.models import UserMovies

from movieRecFlask import recommender_db
from flask import render_template, flash, request,redirect,url_for
from flask_login import login_required

from movieRecFlask.auth.models import User

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
        # movie_col = UserMovies.sql.column('movie')

        # user_movies = UserMovies.query.filter_by(user_io=user_id)
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

        if form.validate_on_submit():
            movie_name = form.movie_name.data

            movie_list = recommender.recommender2(movie_name)

            # If it's a GET request, we just display the basic page with form
            return render_template('movies2.html', movies=movie_list, form=form)

        else:
            return render_template('movies1.html', form=form)


@main.route('/add/movie/<item>', methods=['GET'])
def add_movie(item):
    form = GetRecsForm()
    user_id = current_user.get_id()

    user_movies = UserMovies.query.filter_by(user_id=user_id).all()

    #if request.method == 'POST':

    UserMovies.add_movie1(user_id=user_id, movie=item)
    # movie = str(item)
    # post_entry = UserMovies(user_id=user_id, movie=movie)
    # recommender_db.session.add(post_entry)
    # recommender_db.session.commit()

    flash('Sucessful')

        # user_id = current_user.get_id()
    # stringitem = str(item)
    # #UserMovies.add_movie1(user_id=user_id, movie=item)
    #
    # mov = UserMovies(user_id=user_id, movie=stringitem)
    # recommender_db.session.add(mov)
    # recommender_db.session.commit()
    #
    #
    #
    # flash('Movie Added Successfully!')
    #
    # user_movies = UserMovies.query.filter_by(user_id=user_id).all()


    # If it's a POST request, we get the movie name from user input and run recommender
    # if form.validate_on_submit():
    #     movie_name = form.movie_name.data
    #
    #     movie_list = recommender.recommender2(movie_name)

    return render_template('movie_added.html')
    # else:
    #
    #     return render_template('movies1.html', user_movies=user_movies, form=form)

    # No 'GET' request

# @main.route('/add/movie')
# def add_movie():
#
#     form = GetRecsForm()
#     if form.validate_on_submit():
#
#         flash('Please enter a movie title to get recommendations!')
#
#     movie_name = form.movie_name
#
#     movie_list = recommender.recommender2(movie_name)
#
#     # added_movie = UserMovies(user_id=current_user.get_id, movie=item)
#
#     # recommender_db.session.add(added_movie)
#     # recommender_db.session.commit()
#     # flash('Movie Added!')
#
#     return redirect(url_for('main.getrecs2', user_id=current_user.get_id))


@main.route('/remove/movie/<item>', methods=['GET'])
def remove_movie(item):
    form = GetRecsForm()
    user_id = current_user.get_id()

    user_movies = UserMovies.query.filter_by(user_id=user_id).all()

    #if request.method == 'POST':

    UserMovies.remove_movie1(user_id=user_id, movie=item)
    # movie = str(item)
    # post_entry = UserMovies(user_id=user_id, movie=movie)
    # recommender_db.session.add(post_entry)
    # recommender_db.session.commit()

    flash('Sucessful')

        # user_id = current_user.get_id()
    # stringitem = str(item)
    # #UserMovies.add_movie1(user_id=user_id, movie=item)
    #
    # mov = UserMovies(user_id=user_id, movie=stringitem)
    # recommender_db.session.add(mov)
    # recommender_db.session.commit()
    #
    #
    #
    # flash('Movie Added Successfully!')
    #
    # user_movies = UserMovies.query.filter_by(user_id=user_id).all()


    # If it's a POST request, we get the movie name from user input and run recommender
    # if form.validate_on_submit():
    #     movie_name = form.movie_name.data
    #
    #     movie_list = recommender.recommender2(movie_name)

    return render_template('movie_removed.html')

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
