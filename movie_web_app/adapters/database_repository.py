# database_repository.py
import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie_web_app.domain.model import Movie, Actor, Director, Genre, Review, User
from movie_web_app.adapters.repository import AbstractRepository



class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        self.dataset_of_movies = []

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_actor(self, actor: Actor):
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def add_movie(self, title,year,description,director,actor,genre,runtime,rating,revenue,meta, vote):
        movie = Movie(title,year)
        movie.description = description
        movie.director = Director(director)
        actors = actor.split(",")
        for a in actors:
            movie.add_actor(Actor(a.strip()))
        genres = genre.split(",")
        for g in genres:
            movie.add_genre(Genre(g))
        movie.runtime = runtime
        movie.rating = rating
        if revenue != "N/A":
            movie.revenue = float(revenue)
        if meta != "N/A":
            movie.meta = int(meta)
        movie.vote = vote

        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_actor(self, actor_name) -> Actor:
        actor = None
        try:
            actor = self._session_cm.session.query(Actor).filter_by(actor_full_name=actor_name).all()
        except NoResultFound:
            pass
        return actor

    def get_director(self, director_name) -> Director:
        director = None
        try:
            director = self._session_cm.session.query(Director).filter_by(director_full_name=director_name).all()
        except NoResultFound:
            pass
        return director

    def get_genre(self, genre_name) -> Genre:
        genre = None
        try:
            genre = self._session_cm.session.query(Genre).filter_by(genre_name=genre_name).all()
        except NoResultFound:
            pass
        return genre

    def get_movie(self, title) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter_by(title=title).one()
        except NoResultFound:
            pass
        return movie

    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(user_name=user_name.lower()).one()
        except NoResultFound:
            pass
        return user

    def get_review(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def get_dataset_of_movies(self):
        dataset_of_movies = self._session_cm.session.query(Movie).all()
        return dataset_of_movies


def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            row = [item.strip() for item in row]
            yield row[0:2] + [row[3]] + row[6:]

def director_record_generator(filename:str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            yield [row[1],row[4]]


def actor_record_generator(filename:str,cursor):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            row1 = row[5].split(',')
            insert_actors = """
                   INSERT INTO actors (
                   movie,actor_full_name,rating,rating_num)
                   VALUES (?,?,0,0)"""
            for i in row1:
                cursor.executemany(insert_actors, [[row[1],i.strip()]])


def genre_record_generator(filename:str,cursor):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            row1 = row[2].split(',')
            insert_genres = """
                    INSERT INTO genres (
                    movie,genre_name,rating,rating_num)
                    VALUES (?,?,0,0)"""
            for i in row1:
                cursor.executemany(insert_genres,[[row[1],i.strip()]])


def populate(engine: Engine, data_path: str):
    connect = engine.raw_connection()
    cursor = connect.cursor()

    insert_movies = """
               INSERT INTO movies (
               id,title,description,time,runtime,rating,votes,revenue,metascore)
               VALUES ( ?,?,?,?,?,?,?,?,?)"""
    cursor.executemany(insert_movies, movie_record_generator(data_path))


    insert_directors = """
               INSERT INTO directors (
               movie,director_full_name,rating,rating_num)
               VALUES (?,?,0,0)"""
    cursor.executemany(insert_directors,director_record_generator(data_path))

    genre_record_generator(data_path, cursor)

    actor_record_generator(data_path,cursor)


    connect.commit()
    connect.close()


