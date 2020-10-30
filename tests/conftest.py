import os
import pytest
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from movie_web_app import create_app
import movie_web_app.adapters.repository as repo
from movie_web_app.adapters import memory_repository, database_repository
from movie_web_app.adapters.orm import metadata, map_model_to_tables
from movie_web_app.adapters.memory_repository import MemoryRepository, read_csv_file

TEST_DATA_PATH_MEMORY = os.path.join(os.path.join(os.sep,'Users', 'user', 'Movie_Web_Application_sqlitedb', 'tests', 'data'),'movies.csv')
TEST_DATA_PATH_DATABASE = os.path.join(os.path.join(os.sep,'Users', 'user', 'Movie_Web_Application_sqlitedb', 'tests', 'data'),'movies.csv')

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///movies.db'

@pytest.fixture
def in_memory_repo():
    repo.repo_instance = MemoryRepository()
    read_csv_file(TEST_DATA_PATH_MEMORY, repo.repo_instance)
    return repo.repo_instance


@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield engine
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def empty_session():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'REPOSITORY': 'database',
        'TEST_DATA_PATH': TEST_DATA_PATH_DATABASE,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self):
        return self._client.post(
            '/authentication/login',
            data={'user_name': 'kurisu', 'password': '1234Qwer'}
        )

    def logout(self):
        return self._client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
