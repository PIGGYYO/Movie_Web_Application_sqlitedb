from datetime import date

import pytest

from movie_web_app.authentication import service as service



def test_can_add_user(in_memory_repo):
    new_username = 'Suzuha'
    new_password = 'abcd1A23'

    service.add_user(new_username, new_password, in_memory_repo)

    assert in_memory_repo.get_user(new_username).user_name == 'suzuha'
    assert in_memory_repo.get_user(new_username).password[0:14] =='pbkdf2:sha256:'


def test_cannot_add_user_with_existing_name(in_memory_repo):
    service.add_user('piggyyo', 'abcd1A23', in_memory_repo)
    username = 'piggyyo'
    password = 'abcd1A23'

    with pytest.raises(service.NameNotUniqueException):
        service.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'Nae'
    new_password = 'abcd1A23'

    service.add_user(new_username, new_password, in_memory_repo)

    try:
        service.check_username_password(new_username, new_password, in_memory_repo)
    except service.NotMatchException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'Nae'
    new_password = 'abcd1A23'

    service.add_user(new_username, new_password, in_memory_repo)
    with pytest.raises(service.NotMatchException):
        service.check_username_password(new_username, '0987654321', in_memory_repo)
