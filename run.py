# movieRecFlask/run.py
from movieRecFlask import create_app, recommender_db
from flask_login import UserMixin
from datetime import datetime
from movieRecFlask.auth.models import User, Logins
from movieRecFlask.catalog.models import RecsClicks
from movieRecFlask.plotlydash.dashboard1 import create_dashboard
from sqlalchemy import exc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This is where we run the app. It is outside of the movieRecFlask folder
# by importing the create_app function, we can easily switch between 'dev', 'test' and 'prod'
# runtimes with a quick change here

###################################################################
# - DEFAULT LOCAL HOST SETTINGS - check settings in dashboard1.py as well
###################################################################

# if __name__ == '__main__':
#     flask_app = create_app('dev')
#
#     with flask_app.app_context():
#
#         recommender_db.create_all()
#
#         # If any of the User, RecsClicks or Logins tables are empty in Postgres,
#         # Create an entry for them to initilialize
#         # This is because other functions (Dashboard, etc.) require data in these tables
#         # at start up to be initialize correctly
#         if not User.query.filter_by(user_name='harry').first():
#             User.create_user(user='harry', email='harry@potters.com', password='secret')
#
#         if not RecsClicks.query.filter_by(user_id=0).first():
#             RecsClicks.record_getrecs(user_id=0, movie_id=0, movie='None', comp_score=50.0)
#
#         if not Logins.query.filter_by(userid=0).first():
#             Logins.record_login(userid=0)
#
#         # Dash app functions require these tables above before it can be initiliazed
#         dash_app = create_dashboard(flask_app)
#
#         flask_app.run( debug=True)

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

################################################################
# - WEB HOST SETTINGS - check settings in dashboard1.py as well
################################################################

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
            RecsClicks.record_getrecs(user_id=0, movie_id=0, movie='None', comp_score=50.0)

        if not Logins.query.filter_by(userid=0).first():
            Logins.record_login(userid=0)

        # # Dash app functions require these tables below before it can be initiliazed
        dash_app = create_dashboard(flask_app)

    except exc.IntegrityError:

        flask_app.run()

