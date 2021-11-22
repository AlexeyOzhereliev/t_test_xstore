from rest_framework import serializers


class GenreSerializer(serializers.Serializer):
    genre = serializers.CharField(max_length=255)
    movies_count = serializers.IntegerField(source='id__count')
    avg_rating = serializers.DecimalField(source='imdb_rating__avg', max_digits=2, decimal_places=1)


class ActorsSerializer(serializers.Serializer):
    actor_name = serializers.CharField(max_length=255)
    movies_count = serializers.IntegerField()
    best_genre = serializers.CharField(max_length=255)


class DirectorsSerializer(serializers.Serializer):
    director_name = serializers.CharField(max_length=255)
    favourite_actors = serializers.JSONField()
    best_movies = serializers.JSONField()