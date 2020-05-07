# MovieRecSite/catalog/models.py
from movieRecFlask import recommender_db
from datetime import datetime
from datetime import date

# SQLAlchemy database class/methods

# Tables are created by making a new class of type db.Model

# A db.Model object is a new Table


class UserMovies(recommender_db.Model):

    __tablename__ = 'user_movies'

    # One of the benefits of SQLAlchemy is you can create tables here in Python,
    #    rather than writing SQL in the database platform
    # The ORM (Object Relational Mapper) converts the class definitions to the SQL statements

    id = recommender_db.Column(recommender_db.Integer, primary_key=True)
    user_id = recommender_db.Column(recommender_db.Integer, recommender_db.ForeignKey('users.id'))
    movie = recommender_db.Column(recommender_db.String(80), nullable=False)
    add_date = recommender_db.Column(recommender_db.DateTime, default=datetime.now)

    # in-built python methods
    # __init__() is called when new instances of a class are created, it initializes reference variables and attributes
    # __repr__() takes only 1 parameter, self, and returns a string representation of an instance,
    #                this helps in formatting and producing a readable output of the data

    def __init__(self, user_id, movie):
        self.movie = movie
        self.user_id = user_id

    def __repr__(self):
        return '{}'.format(self.movie)

    @classmethod
    def add_movie1(cls, user_id, movie):
        mov = cls(user_id=user_id, movie=movie)

        recommender_db.session.add(mov)
        recommender_db.session.commit()

        return mov

    @classmethod
    def remove_movie1(cls, user_id, movie):

        UserMovies.query.filter_by(user_id=user_id, movie=movie).delete()
        recommender_db.session.commit()

        return UserMovies.query.filter_by(user_id=user_id)



# RecsClick Table records every time a user or non-user click get recs

class RecsClicks(recommender_db.Model):

    __tablename__ = 'recsclicks'

    # One of the benefits of SQLAlchemy is you can create tables here in Python,
    #    rather than writing SQL in the database platform
    # The ORM (Object Relational Mapper) converts the class definitions to the SQL statements

    # date,userId,movieId,titleSearched,titleReturned,avg-rating

    date = recommender_db.Column(recommender_db.DateTime, primary_key=True, default=datetime.now)
    user_id = recommender_db.Column(recommender_db.Integer)
    movie_id = recommender_db.Column(recommender_db.Integer)
    movie = recommender_db.Column(recommender_db.String(80), nullable=False)

    # in-built python methods
    # __init__() is called when new instances of a class are created, it initializes reference variables and attributes
    # __repr__() takes only 1 parameter, self, and returns a string representation of an instance,
    #                this helps in formatting and producing a readable output of the data

    def __init__(self, user_id, movie_id, movie):
        self.user_id = user_id
        self.movie_id=movie_id
        self.movie = movie


    def __repr__(self):
        return 'Get Recs by {} for movie {} with movieID {}'.format(self.user_id, self.movie, self.movie_id)

    @classmethod
    def record_getrecs(cls, user_id, movie_id, movie):

        getrecsclick = cls(user_id=user_id, movie_id=movie_id, movie=movie)

        recommender_db.session.add(getrecsclick)
        recommender_db.session.commit()

        return getrecsclick

