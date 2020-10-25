# authentication.py
from flask import Blueprint, render_template, redirect, url_for, session, request
import movie_web_app.authentication.service as service
import movie_web_app.adapters.repository as repo

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None

    if form.validate_on_submit():
        try:
            service.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('authentication_bp.login'))
        except service.NameNotUniqueException:
            username_not_unique = 'Your username is already taken - please supply another'
    return render_template(
        'authentication/user_information.html',
        title = 'Register',
        form = form,
        username_error_message = username_not_unique,
        password_error_message = None,
        handler_url=url_for('authentication_bp.register'),
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    no_username = None
    not_match = None

    if form.validate_on_submit():
        try:
            user = service.get_user(form.user_name.data.lower(), repo.repo_instance)
            service.check_username_password(user.user_name, form.password.data, repo.repo_instance)
            session.clear()
            session['username'] = user.user_name

            return redirect(url_for('home_bp.home'))

        except service.NoUserNameException:
            no_username = 'Username not recognised - please supply another'

        except service.NotMatchException:
            not_match = 'Password does not match supplied username'
    return render_template('authentication/user_information.html',
                           title = 'Login',
                           form = form,
                           username_error_message = no_username,
                           password_error_message = not_match)


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Password must be at least 6 characters, and contain an upper case letter, \
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(6) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Username is required'),
        Length(min=3, message='Username is too short')])

    password = PasswordField('Password', [
        DataRequired(message='Password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Username is required')])

    password = PasswordField('Password',[
        DataRequired(message='Password is required')])
    submit = SubmitField('Login')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view
