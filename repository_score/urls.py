from django.urls import path

from repository_score.views import GithubRepositoryScoreViewSet, HealthStatus

urlpatterns = [
    path('repository_is_popular/', GithubRepositoryScoreViewSet.as_view()),
    path('health_status/', HealthStatus.as_view()),
]
