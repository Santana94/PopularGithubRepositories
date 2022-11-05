import logging

import github
from github.GithubException import GithubException, UnknownObjectException
from github.Repository import Repository
from rest_framework.exceptions import ValidationError

from popular_github import settings

logger = logging.getLogger('repository_score')


def get_github_repository(repository_name: str) -> Repository:
    g = github.Github(settings.GITHUB_ACCESS_TOKEN)
    try:
        return g.get_repo(repository_name)
    except UnknownObjectException as e:
        raise ValidationError(detail=f"Repository \"{repository_name}\" not found!")
    except GithubException as e:
        logger.error(e)


def check_repository_score_is_popular(stargazers_count: float, forks_count: int) -> bool:
    score = stargazers_count * 1 + forks_count * 2
    if score >= settings.POPULAR_BASE_SCORE:
        return True
    return False
