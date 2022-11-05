import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("stargazers_count, forks_count, expected_is_popular", [
    (1, 3, False),
    (1, 249, False),
    (0, 250, True),
    (100, 250, True),
])
def test_github_repository_score_view(client, mocker, fake_github, stargazers_count, forks_count, expected_is_popular):
    mocker.patch(
        "repository_score.check_github.github.Github",
        return_value=fake_github(stargazers_count=stargazers_count, forks_count=forks_count)
    )
    response = client.post(reverse("check_repository_is_popular"), data={"repository_name": "something"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'repository_is_popular': expected_is_popular}


def test_github_repository_score_view_unknown_object_exception(
    client, mocker, fake_github_raising_unknown_object_exception
):
    mocker.patch(
        "repository_score.check_github.github.Github",
        return_value=fake_github_raising_unknown_object_exception
    )
    response = client.post(reverse("check_repository_is_popular"), data={"repository_name": "something"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == "Repository \"something\" not found!"


def test_github_repository_score_view_with_github_exception(
    client, mocker, fake_github_raising_github_exception
):
    mocker.patch(
        "repository_score.check_github.github.Github",
        return_value=fake_github_raising_github_exception
    )
    response = client.post(reverse("check_repository_is_popular"), data={"repository_name": "something"})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["detail"] == "Unexpected error when fetching Github API data!"
