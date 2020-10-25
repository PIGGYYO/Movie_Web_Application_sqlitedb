import os
import pytest
import csv

from movie_web_app import create_app
import movie_web_app.adapters.repository as repo
from movie_web_app.adapters.memory_repository import MemoryRepository, read_csv_file
from movie_web_app.domain.model import Movie, Actor, Director, Genre, Review, User

TEST_DATA_PATH = os.path.join(os.sep, 'Users', 'user', 'Movie_Web_Application', 'tests', 'data')


@pytest.fixture
def in_memory_repo():
    repo.repo_instance = MemoryRepository()
    read_csv_file(os.path.join(TEST_DATA_PATH, 'movies.csv'), repo.repo_instance)

    with open(os.path.join(TEST_DATA_PATH, 'users.csv'), mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row == 0:
                continue
            repo.repo_instance.add_user(User(row["username"], row['password']))

    with open(os.path.join(TEST_DATA_PATH, 'reviews.csv'), mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row == 0:
                continue
            movie = repo.repo_instance.get_movie(row['title'])
            user = repo.repo_instance.get_user(row['user'])
            review = Review(user, movie, row['comment-text'], float(row['rating']))
            review.time_stamp = row["timestamp"]
            repo.repo_instance.add_review(review)
            movie.review.append(review)
    return repo.repo_instance


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, user_name='piggyyo', password='cLQ^C#oFXloS5'):
        return self._client.post(
            'authentication/login',
            data={'user_name': 'kurisu', 'password': '1234Qwer'}
        )

    def logout(self):
        return self._client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
