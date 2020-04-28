from movieRecFlask import create_app, recommender_db
from flask_login import UserMixin
from datetime import datetime
from movieRecFlask.auth.models import User
from sqlalchemy import exc

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#######################
# - WEB HOST SETTINGS
#########################

flask_app = create_app('prod')
with flask_app.app_context():
    recommender_db.create_all()

    if not User.query.filter_by(user_name='harry').first():
        User.create_user(user='harry', email='harry@potters.com', password='secret')

    flask_app.run()


# ---------------------------------------------------------------------------------------

#########################
# - LOCAL HOST SETTINGS
##########################

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