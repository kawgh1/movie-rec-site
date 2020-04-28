from movieRecFlask import recommender_db
from datetime import datetime

# SQLAlchemy database class/methods

# Tables are creating by making a new class of type db.Model



# A db.Model object is a new Table
class UserMovies(recommender_db.Model):
    __tablename__ = 'user_movies'

    id = recommender_db.Column(recommender_db.Integer, primary_key=True)
    user_id = recommender_db.Column(recommender_db.Integer, recommender_db.ForeignKey('users.id'))
    movie = recommender_db.Column(recommender_db.String(80), nullable=False)
    add_date = recommender_db.Column(recommender_db.DateTime, default=datetime.now)

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
        # mov = cls(user_id=user_id, movie=movie)
        UserMovies.query.filter_by(user_id=user_id, movie=movie).delete()
        # recommender_db.session.delete(mov)
        recommender_db.session.commit()
        return UserMovies.query.filter_by(user_id=user_id)
