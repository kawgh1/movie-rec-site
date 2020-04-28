import os


DEBUG = False
SECRET_KEY = 'asdf4809uasd908r3q450a987fsdf9043j6l23io6u2nhvgbpo932u5gasdf2q345bhwqe'
# SQLALCHEMY_DATABASE_URI='<database>://<user_id>:<password>@<server>/<database_name>'

# The next line is only relevant for a localhost website,
# SQLALCHEMY_DATABASE_URI='postgresql://postgres:password@localhost/rec_db'

# since we are hosting on the web, we need a different DATABASE_URI

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False

# since these changes were made they were commited to both the local and remote repositories
# 'git add .'
# 'git commit -m "made corrections" '
# 'git push'

