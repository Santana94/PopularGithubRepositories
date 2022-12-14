import pytest
from github import UnknownObjectException, GithubException
from rest_framework.exceptions import ValidationError, APIException

from repository_score import check_github


@pytest.mark.parametrize("stargazers_count, forks_count, expected_is_popular", [
    (1, 3, False),
    (1, 249, False),
    (0, 250, True),
    (100, 250, True),
])
def test_check_repository_score_is_popular(stargazers_count, forks_count, expected_is_popular):
    is_popular = check_github.check_repository_score_is_popular(
        stargazers_count=stargazers_count, forks_count=forks_count
    )
    assert is_popular is expected_is_popular


@pytest.mark.parametrize("stargazers_count, forks_count, expected_score", [
    (1, 3, 7),
    (10, 3, 16),
    (10, 70, 150),
    (1, 249, 499),
    (0, 250, 500),
    (70, 300, 670),
])
def test_get_repository_score(stargazers_count, forks_count, expected_score):
    repository_score = check_github.get_repository_score(
        stargazers_count=stargazers_count, forks_count=forks_count
    )
    assert repository_score == expected_score


def test_get_github_repository(mocker, fake_repository_class):
    fake_get_repo = fake_repository_class(stargazers_count=30, forks_count=10)
    mocker.patch("repository_score.check_github.github_instance.get_repo", return_value=fake_get_repo)
    repository = check_github.get_github_repository(repository_name="Somethinf")

    assert isinstance(repository, fake_repository_class)


def test_get_github_repository_with_unknown_object_exception(mocker):
    mocker.patch(
        "repository_score.check_github.github_instance.get_repo",
        side_effect=UnknownObjectException(data={"message": "something"}, status=404, headers=None)
    )

    with pytest.raises(ValidationError) as error:
        check_github.get_github_repository(repository_name="Something")

    assert error.value.detail[0] == "Repository \"Something\" not found!"


def test_get_github_repository_with_github_exception(mocker):
    github_exception = GithubException(data={"message": "something"}, status=500, headers=None)
    mocked_logger_error = mocker.patch("repository_score.check_github.logger.error")
    mocker.patch(
        "repository_score.check_github.github_instance.get_repo",
        side_effect=github_exception
    )

    with pytest.raises(APIException) as error:
        check_github.get_github_repository(repository_name="Existent")

    assert error.value.detail == "Unexpected error when fetching Github API data!"
    mocked_logger_error.assert_called_with(github_exception)


