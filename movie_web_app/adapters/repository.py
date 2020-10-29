# repository.py
import abc
from typing import List

from movie_web_app.domain.model import Actor, Director, Genre, Movie, Review, User


repo_instance = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        # Adds an actor to repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_name) -> Actor:
        # Returns the Actor named actor_name from the repository.
        # If there is no Actor with the given actor_name, this method returns None.
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        # Adds an director to repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_name) -> Director:
        # Returns the Director named director_name from the repository.
        # If there is no Director with the given director_name, this method returns None.
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        # Adds an genre to repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, genre_name) -> Genre:
        # Returns the Genre named genre_name from the repository.
        # If there is no Genre with the given genre_name, this method returns None.
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, id, title, year, description, director, actor, genre, runtime, rating,revenue,meta,vote):
        # Adds an movie to repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, movie_name) -> Movie:
        # Returns the Movie named movie_name from the repository.
        # If there is no Movie with the given movie_name, this method returns None.
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        # Adds an genre to repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        # Returns the Genre named genre_name from the repository.
        # If there is no Genre with the given genre_name, this method returns None.
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        # Adds an genre to repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self):
        # Returns the Genre named genre_name from the repository.
        # If there is no Genre with the given genre_name, this method returns None.
        raise NotImplementedError


