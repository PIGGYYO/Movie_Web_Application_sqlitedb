import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from movie_web_app.domain.model import User, Movie, Director, Actor, Review, Genre

article_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_user():
    user = User("Andrew", "111")
    return user

def insert_movie(empty_session):
    empty_session.execute(
        """INSERT INTO movies (id,title,description,time,runtime,rating,votes,revenue,metascore) VALUES 
        (1, "Guardians of the Galaxy","A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.",2014,121,8.1,757074,333.13,76)
        """
    )
    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def make_movie():
    movie = Movie('Guardians of the Galaxy', 2014)
    movie.runtime_minutes = 121
    movie.actors = [Actor('Chris Pratt'), Actor('Vin Diesel'), Actor('Bradley Cooper'), Actor('Zoe Saldana')]
    movie.genres = [Genre('Action'), Genre('Adventure'), Genre('Sci-Fi')]
    movie.description = "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    movie.director = [Director('James Gunn')]
    movie.rating = 8.1
    movie.meta = 76
    movie.revenue = 333.13
    movie.vote = 757074
    return movie


def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234"))
    users.append(("cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "1234"),
        User("cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "111")]


def test_loading_of_movie(empty_session):
    movie_key = insert_movie(empty_session)
    expected_movie = make_movie()
    fetched_movie = empty_session.query(Movie).one()

    assert expected_movie == fetched_movie
    assert movie_key == fetched_movie.id