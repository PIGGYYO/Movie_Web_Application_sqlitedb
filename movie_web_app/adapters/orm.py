from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, VARCHAR
)
from sqlalchemy.orm import mapper, relationship

from movie_web_app.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', String(1024), nullable=False),
    Column('movie', ForeignKey('movies.title')),
    Column('actors',ForeignKey('actors.actor_full_name')),
    Column('genres',ForeignKey('genres.genre_name')),
    Column('directors',ForeignKey('directors.director_full_name')),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=True),
    Column('rating', Integer,nullable=True)
)
movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(2048), nullable=False),
    Column('time', Integer, nullable=False),
    Column('runtime', String(1024), nullable=False),
    Column('rating', String(1024), nullable=False),
    Column('votes', String(1024), nullable=False),
    Column('revenue', String(1024), nullable=False),
    Column('metascore', String(1024), nullable=False),
    Column('add_url', String(255), nullable=True)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie', ForeignKey('movies.title')),
    Column('director_full_name', String(255),nullable=False),
    Column('rating', Integer, nullable=True),
    Column('rating_num',Integer, nullable=True),
    Column('add_url', String(255), nullable=True)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie', ForeignKey('movies.title')),
    Column('actor_full_name', String(255),nullable=False),
    Column('rating', Integer, nullable=True),
    Column('rating_num',Integer, nullable=True),
    Column('add_url', String(255), nullable=True)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie', ForeignKey('movies.title')),
    Column('genre_name', String(255),nullable=False),
    Column('rating', Integer, nullable=True),
    Column('rating_num',Integer, nullable=True),
    Column('add_url', String(255), nullable=True)
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        'user_name': users.c.username,
        'password': users.c.password
    })
    mapper(model.Review, reviews, properties={
        'review_text': reviews.c.review,
        'time_stamp': reviews.c.timestamp,
        'user': reviews.c.user,
        'rating': reviews.c.rating
    })
    mapper(model.Movie, movies, properties={
        'title': movies.c.title,
        'description': movies.c.description,
        'director': relationship(model.Director, backref='directors'),
        'genres': relationship(model.Genre, backref='genres'),
        'actors': relationship(model.Actor, backref='actors'),
        'time':movies.c.time,
        'runtime_minutes': movies.c.runtime,
        'rating':movies.c.rating,
        'vote':movies.c.votes,
        'revenue':movies.c.revenue,
        'meta':movies.c.metascore,
        'add_comment_url': movies.c.add_url,
        'review':relationship(model.Review, backref='movies')
    })

    mapper(model.Director, directors, properties ={
        'director_full_name': directors.c.director_full_name,
        'review':relationship(model.Review, backref='review_d'),
        'rating':directors.c.rating,
        'rating_num':directors.c.rating_num,
        'add_comment_url': directors.c.add_url
    })
    mapper(model.Actor, actors, properties={
        'actor_full_name': actors.c.actor_full_name,
        'review': relationship(model.Review, backref='review_a'),
        'rating': actors.c.rating,
        'rating_num': actors.c.rating_num,
        'add_comment_url': actors.c.add_url
    })
    mapper(model.Genre, genres, properties={
        'genre_name': genres.c.genre_name,
        'review':relationship(model.Review, backref='review_g'),
        'rating': genres.c.rating,
        'rating_num': genres.c.rating_num,
        'add_comment_url': genres.c.add_url
    })

