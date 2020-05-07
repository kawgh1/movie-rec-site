# movieRecFlask/run.py
from movieRecFlask import create_app, recommender_db
from flask_login import UserMixin
from datetime import datetime
from movieRecFlask.auth.models import User, Logins
from movieRecFlask.catalog.models import RecsClicks
from movieRecFlask.plotlydash.dashboard import create_dashboard


from sqlalchemy import exc

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This is where we run the app. It is outside of the movieRecFlask folder
# by importing the create_app function, we can easily switch between 'dev', 'test' and 'prod'
# runtimes with a quick change here

################################################################
# - WEB HOST SETTINGS - check settings in dashboard.py as well
################################################################

# flask_app = create_app('prod')
#
# # Create Dash Dashboard app by using the flask_app as its server
# dash_app = create_dashboard(flask_app)
#
# with flask_app.app_context():
#     # create all database tables if they don't already exist
#     recommender_db.create_all()
#
#     # this code says, if user_name 'harry' does not exist in our database
#     # create that user
#
#     # this is needed so that the database doesn't initialize raw with no users to compare to
#     # which can result in database errors if 'no users exist in table' when a user tries to log in
#     # and it is searching for users.
#     try:
#         if not User.query.filter_by(user_name='harry').first():
#             User.create_user(user='harry', email='harry@potters.com', password='secret')
#     except exc.IntegrityError:
#         flask_app.run()


flask_app = create_app('prod')

with flask_app.app_context():

    recommender_db.create_all()


    # If any of the User, RecsClicks or Logins tables are empty in Postgres,
    # Create an entry for them to initilialize
    # This is because other functions (Dashboard, etc.) require data in these tables to be valid
    try:
        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry', email='harry@potters.com', password='secret')

        if not RecsClicks.query.filter_by(user_id=0).first():
            RecsClicks.record_getrecs(user_id=0, movie_id=0, movie='None')

        if not Logins.query.filter_by(userid=0).first():
            Logins.record_login(userid=0)

    except exc.IntegrityError:
        # Dash app functions require these tables above before it can be initiliazed
        dash_app = create_dashboard(flask_app)

        flask_app.run(debug=False)

# ---------------------------------------------------------------------------------------

###################################################################
# - LOCAL HOST SETTINGS - check settings in dashboard.py as well
###################################################################

if __name__ == '__main__':
    flask_app = create_app('dev')

    with flask_app.app_context():

        recommender_db.create_all()


        # If any of the User, RecsClicks or Logins tables are empty in Postgres,
        # Create an entry for them to initilialize
        # This is because other functions (Dashboard, etc.) require data in these tables to be valid
        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry', email='harry@potters.com', password='secret')

        if not RecsClicks.query.filter_by(user_id=0).first():
            RecsClicks.record_getrecs(user_id=0, movie_id=0, movie='None')

        if not Logins.query.filter_by(userid=0).first():
            Logins.record_login(userid=0)

        # Dash app functions require these tables above before it can be initiliazed
        dash_app = create_dashboard(flask_app)

        flask_app.run(debug=True)



#### DASH code
#
# with app.app_context():
    #     # Import Flask routes
    #     from movieRecFlask.catalog import routes
    #
    #     # Import Dash application
    #     from movieRecFlask.plotlydash.dashboard import create_dashboard
    #     app = create_dashboard(app)
    #
    #     # Compile CSS
    #     # from movieRecFlask.assets import compile_assets
    #     # compile_assets(app)