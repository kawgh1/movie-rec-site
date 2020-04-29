# movieRecFlask/auth/routes.py
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from movieRecFlask.auth.forms import RegistrationForm, LoginForm


from movieRecFlask.auth import authentication as at
from movieRecFlask.auth.models import User


@at.route('/register', methods=['GET', 'POST'])
def register_user():

    # if the current user is already logged in and authenticated...
    if current_user.is_authenticated:
        flash('You are already logged in!')
        # then when they click on the log in button, it should not send them to the log in page
        # cause they're already logged in, just send them to the main page instead
        return redirect(url_for('main.hello'))

    # # initial state
    # name = None
    # email = None
    #
    form = RegistrationForm()
    #
    # # basically if it's a POST request, ie the user is sending info to the server
    # # that is, filling out the form and submitting it
    # # do this
    # if request.method == 'POST':
    #     name = form.name.data
    #     email = form.email.data

    # This code is an improvement on the above
    # It uses the form itself to validate
    # instead of whether it's a POST request or not

    # Is it a POST request? If so, check if the data is valid using the validators in auth/forms.py
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        flash('Registration Successful!')
        # if the User just registered, redirect them to the Log In page
        # to log in with the credentials they just created
        return redirect(url_for('authentication.do_the_login'))

    # otherwise it's a GET request and just display the registration.html page below
    # return render_template('registration.html', form=form, name=name, email=email)
    return render_template('registration.html', form=form)


@at.route('/login', methods=['GET', 'POST'])
def do_the_login():

    # if the current user is already logged in and authenticated...
    if current_user.is_authenticated:
        flash('You are already logged in!')
        # then when they click on the log in button, it should not send them to the log in page
        # cause they're already logged in, just send them to the main page instead
        return redirect(url_for('main.hello'))

    # If it's a GET request, then we display the form
    # and we skip all this above and go to the last return, displaying the login.html
    form = LoginForm()

    # If it's a POST request, ie. user is trying to log in!
    # it validates the form data
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()

        # 'if not user' --> means if the 'user' does not exist in the database or
        # password is not valid for the user, flash message and reload login page

        # this user.check_password() method is in the models.py file
        if not user or not user.check_password(form.password.data):
            flash('Invalid Credentials, Please try again.')
            return redirect(url_for('authentication.do_the_login'))

        # if user log in IS valid, display the main page!
        # Write the user credentials to the session and stay logged in for the session
        login_user(user, form.stay_loggedin.data)
        return redirect(url_for('main.hello'))

    return render_template('login.html', form=form)


@at.route('/logout')
@login_required
# we don't need to define any methods ['GET', 'POST'] because log out is always a GET request
def log_out_user():
    logout_user()
    return redirect(url_for('main.hello'))