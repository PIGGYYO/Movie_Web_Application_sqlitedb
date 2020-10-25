# model.py
# Actor, Director, Genre, Movie, Review, User
from datetime import time,datetime


class Actor:
    def __init__(self, actor_full_name):
        self.colleague_list = []
        self.actor_full_name = actor_full_name
        self.review = []
        self.rating = 0
        self.rating_num = 0

    def __repr__(self):
        if self.actor_full_name != "" and isinstance(self.actor_full_name, str):
            return "<{}>".format(self.actor_full_name)
        else:
            return "<None>"

    def __eq__(self, other):
        if other is None:
            return True
        return self.actor_full_name == other.actor_full_name

    def __lt__(self, other):
        return self.actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.actor_full_name)

    def add_actor_colleague(self, colleague):
        self.colleague_list.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.colleague_list


class Director:
    def __init__(self, director):
        self.director_full_name = director
        self.review = []
        self.rating = 0
        self.rating_num = 0

    def __repr__(self):
        if self.director_full_name != "":
            return "<{}>".format(self.director_full_name)
        else:
            return "<None>"

    def __eq__(self, other):
        if other == None:
            return False
        return self.director_full_name == other.director_full_name

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.director_full_name)



class Genre:
    def __init__(self, genre):
        self.genre_name = genre
        self.review = []
        self.rating = 0
        self.rating_num = 0

    def __repr__(self):
        if self.genre_name != "":
            return "<{}>".format(self.genre_name)
        else:
            return "<None>"

    def __eq__(self, other):
        if other is None:
            return True
        return self.genre_name == other.genre_name

    def __lt__(self, other):
        return self.genre_name < other.genre_name

    def __hash__(self):
        return hash(self.genre_name)


class Movie:
    def __init__(self, title, time):
        if time < 1900:
            raise ValueError("")
        self.title = title
        self.time = time
        self.runtime_minutes = 0
        self.actors = []
        self.genres = []
        self.description = ""
        self.director = ""
        self.rating = 0
        self.meta = "N/A"
        self.revenue = "N/A"
        self.vote = 0
        self.review = []
        self.add_comment_url = ''

    def __repr__(self):
        return "<Movie {}, {}>".format(self.title, self.time)

    def __eq__(self, other):
        if other == None:
            return False
        return self.title + str(self.time) == other.title + str(other.time)

    def __lt__(self, other):
        return self.title + str(self.time) < other.title + str(other.time)

    def __hash__(self):
        return hash(self.title + str(self.time))

    def add_actor(self, actor):
        self.actors.append(actor)

    def remove_actor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def add_genre(self, genre):
        self.genres.append(genre)

    def remove_genre(self, genre):
        if genre in self.genres:
            self.genres.remove(genre)

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if runtime_minutes < 0:
            raise ValueError("")
        self.__runtime_minutes = runtime_minutes


class Review:
    def __init__(self, user, movie, review_text, rating):
        self.user = user
        self.movie = movie
        self.review_text = review_text
        if rating >= 0 and rating <= 10:
            self.rating = rating
        else:
            self.rating = None
        self.time_stamp = datetime.today()

    def __repr__(self):
        return ""

    def __eq__(self, other):
        if self.movie == other.movie and self.review_text == other.review_text and self.rating == other.rating and self.time_stamp == other.time_stamp:
            return True
        return False


class User:
    def __init__(self, user_name, password):
        self.user_name = user_name.strip().lower()
        self.password = password
        self.watched_movies = []
        self.reviews = []
        self.time_spent_watching_movies_minutes = 0

    def __repr__(self):
        return "<User {}>".format(self.user_name)

    def __eq__(self, other):
        return self.user_name == other.user_name

    def __lt__(self, other):
        return self.user_name < other.user_name

    def __hash__(self):
        return hash(self.user_name)

    def watch_movie(self, movie):
        if movie not in self.watched_movies and type(movie) is Movie:
            self.watched_movies += [movie]
            self.time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if review not in self.reviews and type(review) is Review:
            self.reviews += [review]

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, time_spent_watching_movies_minutes):
        if time_spent_watching_movies_minutes < 0:
            raise ValueError("")
        self.__time_spent_watching_movies_minutes = time_spent_watching_movies_minutes

    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, user_name):
        if type(user_name) is str:
            self.__user_name = user_name.strip().lower()

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if type(password) is str:
            self.__password = password