from rest_framework import serializers


class GithubRepositorySerializer(serializers.Serializer):
    repository_name = serializers.CharField(max_length=256)
