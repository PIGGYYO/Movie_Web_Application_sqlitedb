from datetime import date, datetime

import pytest

from movie_web_app.adapters.database_repository import SqlAlchemyRepository
from movie_web_app.domain.model import User, Movie, Director, Actor, Review, Genre

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('martin', '123456789'))
    user = repo.get_user('martin')
    assert user == User('martin', '123456789')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
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

    repo.add_movie(1,'Guardians of the Galaxy', 2014, movie.description, 'James Gunn',
                             'Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana', 'Action,Adventure,Sci-Fi',
                             movie.runtime_minutes, movie.rating, movie.revenue, movie.meta, movie.vote)

    assert repo.get_movie("Guardians of the Galaxy") == movie


def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie('Prometheus')

    assert movie.title == 'Prometheus'


def test_repository_does_not_retrieve_a_non_existent_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie('?')
    assert movie is None


def test_repository_can_add_a_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    director = Director('Aoba')
    repo.add_director(director)
    director1 = repo.get_director('Aoba')[0]
    assert director1 == director and director1 is director


def test_repository_does_not_retrieve_a_non_existent_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    director = repo.get_director('?')
    assert director == []


def test_repository_can_add_a_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    actor = Actor('Aoba')
    repo.add_actor(actor)
    actor1 = repo.get_actor('Aoba')[0]
    assert actor1 == actor and actor1 is actor


def test_repository_does_not_retrieve_a_non_existent_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    actor = repo.get_actor('?')
    assert actor == []


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = Genre('Aoba')
    repo.add_genre(genre)
    genre1 = repo.get_genre('Aoba')[0]
    assert genre1 == genre and genre1 is genre


def test_repository_does_not_retrieve_a_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = repo.get_genre('?')
    assert genre == []


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    repo.add_user(user)
    review = Review('Dave', 'Prometheus', None,None,None,'?', 8)
    repo.add_review(review)
    review1 = repo.get_review()[0]
    assert review == review1 and review1 is review
