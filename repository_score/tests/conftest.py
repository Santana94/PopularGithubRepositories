from collections import namedtuple

import pytest


@pytest.fixture
def fake_repository_class():
    return namedtuple("FakeRepository", "stargazers_count, forks_count")
