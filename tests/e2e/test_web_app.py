import pytest

from flask import session
from movie_web_app.domain.model import Movie, Actor, Director, Genre, Review, User


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    response = client.post(
        '/authentication/register',
        data={'user_name': 'kurisu', 'password': '1234Qwer'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'

'''
@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required'),
        ('1', '1', b'Username is too short'),
        ('test', '', b'Password is required'),
        ('test', 'test', b'Password must be at least 6 characters, and contain an upper case letter, \
            a lower case letter and a digit'),
        ('kurisu', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
'''


def test_login(client, auth,in_memory_repo):
    client.post(
        '/authentication/register',
        data={'user_name': 'kurisu', 'password': '1234Qwer'}
    )
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['username'] == 'kurisu'


def test_logout(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'kurisu', 'password': '1234Qwer'}
    )
    auth.login()

    with client:
        auth.logout()
        assert 'username' not in session


def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_comment(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'kurisu', 'password': '1234Qwer'}
    )
    auth.login()
    response = client.get('/comment?title=Guardians+of+the+Galaxy')
    response = client.post(
        '/comment?title=Guardians+of+the+Galaxy',
        data={'comment': '=w=?ss', 'rating': '10', 'title': 'Guardians of the Galaxy'}
    )
    assert response.headers['Location'] == 'http://localhost/display?title=Review&movie_title=Guardians+of+the+Galaxy'


@pytest.mark.parametrize(('comment', 'rating','messages'), (
        ('Hey', '10',(b'Your comment is too short')),
        ('ass', '',(b'Rating is required'))))
def test_comment_with_invalid_input(client, auth, comment,rating,messages):
    client.post(
        '/authentication/register',
        data={'user_name': 'kurisu', 'password': '1234Qwer'}
    )
    auth.login()

    response = client.post(
        '/comment?title=Guardians+of+the+Galaxy',
        data={'comment': comment, 'rating': rating, 'title': 'Guardians of the Galaxy'}
    )
    for message in messages:
        assert message in response.data


def test_movie_with_actor(client):
    response = client.post(
        '/search_by_actor',
        data={'name1': 'Noomi Rapace', 'name2': 'Logan Marshall-Green', 'name3': '/'}
    )
    assert response.headers['Location'] == 'http://localhost/display?title=Actor&name1=%3CNoomi+Rapace%3E&name2=%3CLogan+Marshall-Green%3E'


def test_movie_with_genre(client):
    response = client.post(
        '/search_by_genre',
        data={'name1': 'Action', 'name2': 'Adventure', 'name3': '/'}
    )
    assert response.headers['Location'] == 'http://localhost/display?title=Genre&name1=%3CAction%3E&name2=%3CAdventure%3E'


def test_movie_with_director(client):
    response = client.post(
        '/search_by_director',
        data={'director_full_name': 'Ridley Scott'}
    )
    assert response.headers['Location'] == 'http://localhost/display?title=Director&name1=%3CRidley+Scott%3E'


def test_comment_actor(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'kurisu', 'password': '1234Qwer'}
    )
    auth.login()
    response = client.get('/comment_actor?title=Chris+Pratt')
    response = client.post(
        '/comment_actor?title=Chris+Pratt',
        data={'comment': '=w=?ss', 'rating': '10', 'title': 'Chris Pratt'}
    )
    assert response.headers['Location'] == 'http://localhost/display_actor?title=Review_Actor&name=Chris+Pratt'


def test_comment_genre(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'kurisu', 'password': '1234Qwer'}
    )
    auth.login()
    response = client.get('/comment_genre?title=Action')
    response = client.post(
        '/comment_genre?title=Action',
        data={'comment': '=w=?ss', 'rating': '10', 'title': 'Action'}
    )
    assert response.headers['Location'] == 'http://localhost/display_genre?title=Review_Genre&name=Action'


def test_comment_director(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'kurisu', 'password': '1234Qwer'}
    )
    auth.login()
    response = client.get('/comment_director?title=James+Gunn')
    response = client.post(
        '/comment_director?title=James+Gunn',
        data={'comment': '=w=?ss', 'rating': '10', 'title': 'James Gunn'}
    )
    assert response.headers['Location'] == 'http://localhost/display_director?title=Review_Genre&name=James+Gunn'

