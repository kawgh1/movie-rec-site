# Production configuration for web host

import os


DEBUG = False
SECRET_KEY = 'asdf4809uasd908r3q450a987fsdf9043j6l23io6u2nhvgbpo932u5gasdf2q345bhwqe'
# SQLALCHEMY_DATABASE_URI='<database>://<user_id>:<password>@<server>/<database_name>'

# The next line is only relevant for a localhost website,
# SQLALCHEMY_DATABASE_URI='postgresql://postgres:secret@localhost/recommender_db'

# since we are hosting on Heroku, we need to use the DATABASE_URI native to Heroku
# 'import os' here means import Heroku's os environment, not our local.

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False


