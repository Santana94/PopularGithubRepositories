import pytest
from django.urls import reverse
from django.utils import timezone
from github import UnknownObjectException, GithubException
from rest_framework import status


@pytest.mark.parametrize("stargazers_count, forks_count, expected_is_popular", [
    (1, 3, False),
    (1, 249, False),
    (0, 250, True),
    (100, 250, True),
])
def test_github_repository_score_view(
    client, mocker, fake_repository_class, stargazers_count, forks_count, expected_is_popular
):
    fake_get_repo = fake_repository_class(stargazers_count=stargazers_count, forks_count=forks_count)
    mocker.patch(
        "repository_score.check_github.github_instance.get_repo", return_value=fake_get_repo
    )
    response = client.get(reverse("check_repository_is_popular") + "?repository_name=something")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'repository_is_popular': expected_is_popular}


@pytest.mark.parametrize("query_params, expected_status_code, expected_response_data", [
    ("?repository_name=something", status.HTTP_200_OK, {'repository_is_popular': False}),
    ("?something=something", status.HTTP_400_BAD_REQUEST, {'repository_name': ['This field is required.']}),
    ("?repository_name=", status.HTTP_400_BAD_REQUEST, {'repository_name': ['This field may not be blank.']}),
])
def test_github_repository_score_view_payload(
    client, mocker, fake_repository_class, expected_status_code, query_params, expected_response_data
):
    mocker.patch(
        "repository_score.check_github.github_instance.get_repo",
        return_value=fake_repository_class(stargazers_count=30, forks_count=10)
    )
    response = client.get(reverse("check_repository_is_popular") + query_params)
    assert response.status_code == expected_status_code
    assert response.data == expected_response_data


def test_github_repository_score_view_unknown_object_exception(client, mocker):
    mocker.patch(
        "repository_score.check_github.github_instance.get_repo",
        side_effect=UnknownObjectException(data={"message": "something"}, status=404, headers=None)
    )
    response = client.get(reverse("check_repository_is_popular") + "?repository_name=something")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == "Repository \"something\" not found!"


def test_github_repository_score_view_with_github_exception(client, mocker):
    mocker.patch(
        "repository_score.check_github.github_instance.get_repo",
        side_effect=GithubException(data={"message": "something"}, status=500, headers=None)
    )
    response = client.get(reverse("check_repository_is_popular") + "?repository_name=something")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["detail"] == "Unexpected error when fetching Github API data!"


def test_health_status_view(client, freezer):
    response = client.get(reverse("health_status"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'is_healthy': True,
        'time': timezone.now()
    }
