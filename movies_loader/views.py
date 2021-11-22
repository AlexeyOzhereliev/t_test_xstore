from django.db.models import Count, Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection

from .models import Movie
from .serializers import GenreSerializer, ActorsSerializer, DirectorsSerializer


class GetGenreInfoView(APIView):
    def get(self, request):
        queryset = Movie.objects.values('genre').distinct().annotate(Count('id'), Avg('imdb_rating'))
        serializer_for_queryset = GenreSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data[:20])


class GetActorsInfoView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT name, COUNT(title), genre, MAX(avg_rating)
            FROM(SELECT name, title, genre, AVG(imdb_rating) avg_rating
            FROM movies_loader_movie
            JOIN movies_loader_movie_actors ON movies_loader_movie.id = movies_loader_movie_actors.movie_id
            JOIN movies_loader_actor ON movies_loader_movie_actors.actor_id = movies_loader_actor.id
            GROUP BY genre)
            GROUP BY name
            HAVING name NOTNULL
            LIMIT 20''')
            rows = cursor.fetchall()
            res = []
            keys = ('actor_name', 'movies_count', 'best_genre')
            for row in rows[:20]:
                res.append(dict(zip(keys, row)))
            serializer_for_res = ActorsSerializer(instance=res, many=True)
            return Response(serializer_for_res.data)


class GetDirectorsInfoView(APIView):
    def get(self, request):
        cur = connection.cursor()
        cur.execute('''SELECT director, actor, COUNT(*) as movie_count 
        FROM (SELECT director, title
        FROM movies_loader_movie
        GROUP BY director, title) t1
        JOIN
        (SELECT name as actor, title
        FROM movies_loader_movie
        JOIN movies_loader_movie_actors ON movies_loader_movie.id = movies_loader_movie_actors.movie_id
        JOIN movies_loader_actor ON movies_loader_movie_actors.actor_id = movies_loader_actor.id
        GROUP BY name, title) t2
        on t1.title = t2.title
        GROUP BY director, actor
        HAVING director NOTNULL
        ORDER BY director, movie_count DESC
        LIMIT 100''')

        rows = cur.fetchall()

        cur = connection.cursor()
        cur.execute('''SELECT director, title
        FROM movies_loader_movie
        GROUP BY director, title
        HAVING director NOTNULL
        ORDER BY director, imdb_rating DESC
        LIMIT 20''')

        movie_row = cur.fetchall()
        res = []
        temp_dict = {}
        keys = ('director_name', 'favourite_actors', 'best_movies')
        for row in rows:
            if len(res) == 0 or res[-1]['director_name'] != row[0]:
                temp_dict[keys[0]] = row[0]
                temp_dict[keys[1]] = [{'name': row[1], 'movies_count': row[2]}]
                temp_dict[keys[2]] = []
                res.append(temp_dict)
                temp_dict = {}
            else:
                if len(res[-1]['favourite_actors']) < 3:
                    res[-1]['favourite_actors'].extend([{'name': row[1], 'movies_count': row[2]}])

        res_idx = 0
        for idx in range(len(movie_row)):
            if len(res[res_idx][keys[2]]) < 3 and res[res_idx][keys[0]] == movie_row[idx][0]:
                res[res_idx][keys[2]].extend([movie_row[idx][1]])
            else:
                res_idx += 1
                res[res_idx][keys[2]].extend([movie_row[idx][1]])
        serializer_for_res = DirectorsSerializer(instance=res, many=True)
        return Response(serializer_for_res.data[:20])
