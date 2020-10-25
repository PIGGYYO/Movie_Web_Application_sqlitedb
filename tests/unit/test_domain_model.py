from movie_web_app.domain.model import Movie, Actor, Director, Genre, Review, User

import pytest

@pytest.fixture()
def movie():
    movie = Movie('Guardians of the Galaxy',2014)
    movie.runtime_minutes = 121
    movie.actors = [Actor('Chris Pratt'),Actor('Vin Diesel'),Actor('Bradley Cooper'),Actor('Zoe Saldana')]
    movie.genres = [Genre('Action'),Genre('Adventure'),Genre('Sci-Fi')]
    movie.description = "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    movie.director = Director('James Gunn')
    movie.rating = 8.1
    movie.meta = 76
    movie.revenue = 333.13
    movie.vote = 757074
    return movie


@pytest.fixture()
def user():
    return User('piggyyo', '1234567890')


@pytest.fixture()
def review1():
    return Review(user, movie, 'Hello World', 29)


@pytest.fixture()
def review2():
    return Review(user, movie, 'Hello World', 7)


@pytest.fixture()
def actor():
    return Actor('Kurisu Makise')


@pytest.fixture()
def director():
    return Director('Maho Hiyajo')


@pytest.fixture()
def genre():
    return Genre('Idol')

def test_user_construction(user):
    assert user.user_name == 'piggyyo'
    assert user.password == '1234567890'
    assert repr(user) == '<User piggyyo>'

    for review in user.reviews:
        assert False


def test_article_construction(movie):
    assert movie.title == 'Guardians of the Galaxy'
    assert movie.time  == 2014
    assert movie.runtime_minutes == 121
    assert movie.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    assert movie.genres == [Genre('Action'),Genre('Adventure'),Genre('Sci-Fi')]
    assert movie.actors == [Actor('Chris Pratt'),Actor('Vin Diesel'),Actor('Bradley Cooper'),Actor('Zoe Saldana')]
    assert movie.director == Director('James Gunn')
    assert movie.rating == 8.1
    assert movie.meta == 76
    assert movie.revenue == 333.13
    assert movie.vote == 757074

    assert repr(movie) == '<Movie Guardians of the Galaxy, 2014>'


def test_review_construction_out_of_range(review1):
    assert review1.user == user
    assert review1.movie == movie
    assert review1.review_text == 'Hello World'
    assert review1.rating is None


def test_review_construction(review2):
    assert review2.user == user
    assert review2.movie == movie
    assert review2.review_text == 'Hello World'
    assert review2.rating == 7


def test_actor_construction(actor):
    assert actor.actor_full_name == 'Kurisu Makise'
    assert repr(actor) == '<Kurisu Makise>'


def test_director_construction(director):
    assert director.director_full_name == 'Maho Hiyajo'
    assert repr(director) == '<Maho Hiyajo>'

def test_genre_construction(genre):
    assert genre.genre_name == 'Idol'
    assert repr(genre) == '<Idol>'

