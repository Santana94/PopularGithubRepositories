import logging

import github
from github.GithubException import GithubException, UnknownObjectException
from github.Repository import Repository
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException

from popular_github.settings import settings

logger = logging.getLogger('repository_score')


def get_github_repository(repository_name: str) -> Repository:
    g = github.Github(settings.GITHUB_ACCESS_TOKEN)
    try:
        return g.get_repo(repository_name)
    except UnknownObjectException:
        raise ValidationError(detail=f"Repository \"{repository_name}\" not found!")
    except GithubException as e:
        logger.error(e)
        raise APIException(detail="Unexpected error when fetching Github API data!")


def get_repository_score(stargazers_count: int, forks_count: int) -> int:
    return stargazers_count * 1 + forks_count * 2


def check_repository_score_is_popular(stargazers_count: int, forks_count: int) -> bool:
    if get_repository_score(stargazers_count=stargazers_count, forks_count=forks_count) >= settings.POPULAR_BASE_SCORE:
        return True
    return False
