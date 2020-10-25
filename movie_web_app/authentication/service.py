# service.py
from werkzeug.security import generate_password_hash, check_password_hash

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.model import User


def add_user(user_name, password, repo: AbstractRepository):
    user = repo.get_user(user_name.lower())
    if user is not None:
        raise NameNotUniqueException

    password_hash = generate_password_hash(password)

    user = User(user_name, password_hash)
    repo.add_user(user)


def get_user(user_name,repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise NoUserNameException
    else:
        return user


def check_username_password(user_name, password, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if not check_password_hash(user.password, password):
        raise NotMatchException


class NameNotUniqueException(Exception):
    pass


class NoUserNameException(Exception):
    pass


class NotMatchException(Exception):
    pass
