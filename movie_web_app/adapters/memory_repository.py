# memory_repository.py
import csv
from abc import ABC

from movie_web_app.domain.model import Movie, Actor, Director, Genre, Review, User
from movie_web_app.adapters.repository import AbstractRepository



class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.dataset_of_movies = []
        self.dataset_of_actors = []
        self.dataset_of_directors = []
        self.dataset_of_genres = []
        self.users = []
        self.reviews = []
        self.tags = []

    def add_actor(self, actor: Actor):
        if actor not in self.dataset_of_actors:
            self.dataset_of_actors.append(actor)

    def add_director(self, director: Director):
        if director not in self.dataset_of_directors:
            self.dataset_of_directors.append(director)

    def add_genre(self, genre: Genre):
        if genre not in self.dataset_of_genres:
            self.dataset_of_genres.append(genre)

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
        self.dataset_of_movies.append(movie)

    def add_user(self, user: User):
        self.users.append(user)

    def add_review(self, review: Review):
        self.reviews.append(review)

    def get_actor(self, actor_name) -> Actor:
        return next((actor for actor in self.dataset_of_actors if actor.actor_full_name == actor_name), None)

    def get_director(self, director_name) -> Director:
        return next((director for director in self.dataset_of_directors if director.director_full_name == director_name), None)

    def get_genre(self, genre_name) -> Director:
        return next((genre for genre in self.dataset_of_genres if genre.genre_name == genre_name), None)

    def get_movie(self, title) -> Movie:
        return next((movie for movie in self.dataset_of_movies if movie.title == title), None)

    def get_user(self, user_name) -> User:
        return next((user for user in self.users if user.user_name == user_name.lower()), None)

    def get_review(self):
        return self.reviews


def read_csv_file(filename: str, repo: MemoryRepository):
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row == 0:
                continue
            repo.add_movie(row["Title"], int(row["Year"]), row["Description"], row["Director"],row["Actors"], row["Genre"], row["Runtime (Minutes)"], row["Rating"], row["Revenue (Millions)"], row["Metascore"], row["Votes"])

            actors = row["Actors"].split(",")
            for a in actors:
                repo.add_actor(Actor(a.strip()))

            director = row["Director"]
            repo.add_director(Director(director))

            genres = row["Genre"].split(",")
            for g in genres:
                repo.add_genre(Genre(g))
