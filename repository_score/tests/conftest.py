from collections import namedtuple

import pytest
from github import UnknownObjectException, GithubException


@pytest.fixture
def fake_repository_class():
    return namedtuple("FakeRepository", "stargazers_count, forks_count")


@pytest.fixture
def fake_github_class():
    return namedtuple("FakeGithub", "get_repo")


@pytest.fixture
def fake_github(fake_repository_class, fake_github_class):
    def get_fake_github(stargazers_count: int = 10, forks_count: int = 30):
        return fake_github_class(
            get_repo=lambda name: fake_repository_class(stargazers_count=stargazers_count, forks_count=forks_count)
        )
    return get_fake_github


@pytest.fixture
def fake_github_raising_unknown_object_exception(fake_github_class):
    def get_repo(name):
        raise UnknownObjectException(data={"message": "something"}, status=404, headers=None)

    return fake_github_class(get_repo=get_repo)


@pytest.fixture
def github_exception():
    return GithubException(data={"message": "something"}, status=404, headers=None)


@pytest.fixture
def fake_github_raising_github_exception(github_exception, fake_github_class):
    def get_repo(name):
        raise github_exception

    return fake_github_class(get_repo=get_repo)
