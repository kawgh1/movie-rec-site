# movieRecFlask/run.py
from movieRecFlask import create_app, recommender_db
from flask_login import UserMixin
from datetime import datetime
from movieRecFlask.auth.models import User
from sqlalchemy import exc

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This is where we run the app. It is outside of the movieRecFlask folder
# by importing the create_app function, we can easily switch between 'dev', 'test' and 'prod'
# runtimes with a quick change here

#######################
# - WEB HOST SETTINGS
#######################

flask_app = create_app('prod')
with flask_app.app_context():
    # create all database tables if they don't already exist
    recommender_db.create_all()

    # this code says, if user_name 'harry' does not exist in our database
    # create that user

    # this is needed so that the database doesn't initialize raw with no users to compare to
    # which can result in database errors if 'no users exist in table' when a user tries to log in
    # and it is searching for users.
    try:
        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry', email='harry@potters.com', password='secret')
    except exc.IntegrityError:
        flask_app.run()


# ---------------------------------------------------------------------------------------

#########################
# - LOCAL HOST SETTINGS
#########################

# if __name__ == '__main__':
#     flask_app = create_app('dev')
#     with flask_app.app_context():
#
#         recommender_db.create_all()
#
#         if not User.query.filter_by(user_name='harry').first():
#             User.create_user(user='harry', email='harry@potters.com', password='secret')
#
#         flask_app.run(debug=True)
