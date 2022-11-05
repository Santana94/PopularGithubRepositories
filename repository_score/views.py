from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from repository_score import serializers
from . import check_github


class GithubRepositoryScoreViewSet(APIView):
    def get(self, request):
        repository_serializer = serializers.GithubRepositorySerializer(data=request.POST)
        repository_serializer.is_valid(raise_exception=True)
        github_repository = check_github.get_github_repository(
            repository_name=repository_serializer.data["repository_name"]
        )
        repository_is_popular = check_github.check_repository_score_is_popular(
            stargazers_count=github_repository.stargazers_count, forks_count=github_repository.forks_count
        )
        return Response(status=status.HTTP_200_OK, data={"repository_is_popular": repository_is_popular})


class HealthStatus(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data={"is_healthy": True, "time": timezone.now()})
