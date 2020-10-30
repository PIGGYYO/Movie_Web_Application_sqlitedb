from datetime import date, datetime
from typing import List

import pytest

from movie_web_app.domain.model import Movie, Actor, Director, Genre, Review, User


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Mayuri', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Mayuri') is user


def test_repository_can_add_movie(in_memory_repo):
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

    in_memory_repo.add_movie(1,'Guardians of the Galaxy',2014,movie.description,'James Gunn', 'Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana', 'Action,Adventure,Sci-Fi',movie.runtime_minutes,movie.rating,movie.revenue,movie.meta,movie.vote)

    assert in_memory_repo.get_movie("Guardians of the Galaxy") == movie




def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie("Guardians of the Galaxy")
    assert movie is None


def test_repository_can_add_actor(in_memory_repo):
    actor = Actor("Moeka Kiriyu")
    in_memory_repo.add_actor(actor)

    assert in_memory_repo.get_actor("Moeka Kiriyu") is actor


def test_repository_can_retrieve_actor(in_memory_repo):
    actor = in_memory_repo.get_actor("Scarlett Johansson")

    assert actor.actor_full_name == 'Scarlett Johansson'


def test_repository_does_not_retrieve_a_non_existent_actor(in_memory_repo):
    actor = in_memory_repo.get_actor("Moeka Kiriyu")
    assert actor is None


def test_repository_can_add_director(in_memory_repo):
    director = Director("Rumiho Akiha")
    in_memory_repo.add_director(director)

    assert in_memory_repo.get_director("Rumiho Akiha") is director


def test_repository_can_retrieve_director(in_memory_repo):
    director = in_memory_repo.get_director("Ridley Scott")

    assert director.director_full_name == 'Ridley Scott'


def test_repository_does_not_retrieve_a_non_existent_director(in_memory_repo):
    director = in_memory_repo.get_director("Rumiho Akiha")
    assert director is None



def test_repository_can_add_genre(in_memory_repo):
    genre = Genre("Idol")
    in_memory_repo.add_genre(genre)

    assert in_memory_repo.get_genre("Idol") is genre


def test_repository_can_retrieve_genre(in_memory_repo):
    genre= in_memory_repo.get_genre("Action")

    assert genre.genre_name == 'Action'


def test_repository_does_not_retrieve_a_non_existent_genre(in_memory_repo):
    genre = in_memory_repo.get_genre("Idol")
    assert genre is None



