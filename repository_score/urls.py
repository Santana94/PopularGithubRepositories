from django.urls import path

from repository_score import swagger
from repository_score.views import GithubRepositoryScoreViewSet, HealthStatus

urlpatterns = [
    path('check_repository_is_popular/', GithubRepositoryScoreViewSet.as_view(), name="check_repository_is_popular"),
    path('health_status/', HealthStatus.as_view(), name="health_status"),
    path('docs/', swagger.schema_view),
]
