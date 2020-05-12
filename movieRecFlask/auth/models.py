# movieRecFlask/auth/models.py
from datetime import datetime
from datetime import date
from movieRecFlask import recommender_db, bcrypt # MovieRecSite/__init__.py
from movieRecFlask import login_manager

# UserMixin Class works with the database models
# UserMixin Class has attributes for users such as
#   'get_id', 'is_active', 'is_anonymous' and 'is_authenticated'
# all boolean values that can be used to control access
from flask_login import UserMixin

# A db.Model object is a new Table


class User(UserMixin, recommender_db.Model):
    __tablename__ = 'users'

    id = recommender_db.Column(recommender_db.Integer, primary_key=True)
    user_name = recommender_db.Column(recommender_db.String(20))
    user_email = recommender_db.Column(recommender_db.String(60), unique=True, index=True)
    user_password = recommender_db.Column(recommender_db.String(80))
    # this datetime is from the Python library (and not SQLAlchemy) and needs to be imported above
    registration_date = recommender_db.Column(recommender_db.DateTime, default=datetime.now)

    # in-built python methods
    # __init__() is called when new instances of a class are created, it initializes reference variables and attributes
    # __repr__() takes only 1 parameter, self, and returns a string representation of an instance,
    #                this helps in formatting and producing a readable output of the data

    def __init__(self, user_name, user_email, user_password):

        # user id and registration date have been left out because they are automatically generated and can't be changed
        # they will render on their own in the database table
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password

    def __repr__(self):
        return 'user is {}'.format(self.user_name)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    # class methods belong to a class but are not associated with any class instance
    # ie. this method is belonging to the class User above, and not any particular instance of the class User

    @classmethod
    def create_user(cls, user, email, password):

        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8')
                   )

        recommender_db.session.add(user)
        recommender_db.session.commit()
        return user

# This is just an instance of the login_manager imported at top
@login_manager.user_loader
def load_user(id):
    # gets the UserID from the user table and returns the ID as an int
    # Flask-Login then stores the active user's ID in the session
    return User.query.get(int(id))



#####################################
# This Table is just for the Dashboard app to track user logins to display in the Dashboard


class Logins(UserMixin, recommender_db.Model):
    __tablename__ = 'logins'

    date = recommender_db.Column(recommender_db.DateTime, primary_key=True, default=datetime.now)
    userid = recommender_db.Column(recommender_db.Integer)

    # in-built python methods
    # __init__() is called when new instances of a class are created, it initializes reference variables and attributes
    # __repr__() takes only 1 parameter, self, and returns a string representation of an instance,
    #                this helps in formatting and producing a readble output of the data

    def __init__(self, userid):

        #  date has been left out because it is automatically generated and can't be changed
        # it will render on its own in the database table
        self.userid = userid

    def __repr__(self):
        return 'userId is {}'.format(self.userid)


    # This method records the login in the logins table
    @classmethod
    def record_login(cls, userid):
        userid = cls(userid=userid)

        recommender_db.session.add(userid)
        recommender_db.session.commit()
        return userid
