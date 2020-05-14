# movieRecFlask/__init__.py


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# LoginManager is a class which has all the options we need to manage user logins and sessions
from flask_login import LoginManager
# More flask loginmanager info
# https://flask-login.readthedocs.io/en/latest

# Bcrypt is used for password hashing
# Rather than saving the user's password in plaintext, it saves a hash of the user's password
# This mean's the user's password is never on the website's server
from flask_bcrypt import Bcrypt
# More password security info/methods
# https://flask-bcrypt.readthedocs.io/en/latest

# pip3 install flask-bootstrap

# Twitter Bootstrap is a framework that enables building responsive websites
# using HTML, CSS and Javascript
# http://getbootstrap.com
# For this project we're going to use the Flask version of bootstrap
# because it's more integrated with the Flask framework
# pip3 install flask-bootstrap
from flask_heroku import Heroku

recommender_db = SQLAlchemy()

# create an instance of Bootstrap
bootstrap = Bootstrap()
# create an instance of LoginManager
login_manager = LoginManager()

# this line just tells Flask LoginManager what function we are using to log in
login_manager.login_view = 'authentication.do_the_login'


login_manager.session_protection = 'strong'
# create an instance of Bcrypt
bcrypt = Bcrypt()
heroku = Heroku()


def create_app(config_type):  # dev, test, prod

    app = Flask(__name__)

    # for local work
    # os.getcwd() --> get current working directory --> C:\\Users\<name>\<projects>\<project file>

    # config_type is the name of our package file (dev, test, prod)

    # so we are joining the current working directory with the package folder/file we want
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')

    # This format allows us to change our configuration file with ease,
    # we just pass the file type (dev, test, prod) we want
    # into the create_app(config_type) method in run.py

    app.config.from_pyfile(configuration)

    # Since the config file is now available to us, we can attach it to our database initialization

    recommender_db.init_app(app)  # bind database to flask app

    bootstrap.init_app(app)  # initialize bootstrap, this will integrate bootstrap with our flask application

    login_manager.init_app(app)  # initialize login manager

    bcrypt.init_app(app)  # initialize bcrypt

    heroku.init_app(app)  # initialize heroku

    # from movieRecFlask.catalog import main
    from movieRecFlask.catalog import main  # import 'main' (catalog) blueprint

    # this is the Flask application instance and not the package
    app.register_blueprint(main)  # register blueprint

    # importing the authentication Blueprint from bookFlask.auth
    # not doing this results in a 404 error for localhost/register
    from movieRecFlask.auth import authentication
    app.register_blueprint(authentication)  # import 'authentication' (auth) blueprint

    return app

    # this function above can be called an 'application factory'

    # because we are creating the Flask application on the fly (in run.py) using th desired configuration
    # the configuration can be development, testing or production or other as needed
