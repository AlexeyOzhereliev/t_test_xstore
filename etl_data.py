import os
import sys
from collections import defaultdict
import sqlite3

import pandas as pd

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'

import django

django.setup()

from movies_loader.models import Actor, Writer, Movie

imported_tables = []


def extract():
    conn = sqlite3.connect('outer_db.sqlite')
    queries = ["SELECT * FROM actors",
               "SELECT * FROM writers",
               "SELECT * FROM movies",
               "SELECT * FROM movie_actors",
               ]

    for query in queries:
        table = pd.read_sql_query(f"{query}", conn)
        imported_tables.append(table.to_dict('index'))


def transform():
    global actors, writers, movie_actors, movie_writers, movies

    actors = []
    for key in imported_tables[0]:
        if imported_tables[0][key]['name'] == 'N/A':
            del imported_tables[0][key]['name']
        actors.append(imported_tables[0][key])

    writers = []
    for key in imported_tables[1]:
        if imported_tables[1][key]['name'] == 'N/A':
            del imported_tables[1][key]['name']
        writers.append(imported_tables[1][key])

    movies = []
    movie_writers = []
    for movie_dict in imported_tables[2].values():
        del movie_dict['ratings']
        if movie_dict['writer'] == '':
            del movie_dict['writer']
            copy = movie_dict['writers']
            movie_dict['writers'] = []
            for writer_id in copy.split(','):
                clear_id = writer_id.lstrip('[{"id": "')
                clear_id = clear_id.rstrip('"}]')
                movie_dict['writers'].append(clear_id)
        else:
            movie_dict['writers'] = movie_dict.pop('writer').split()
        movie_writers.append(dict(movie_id=movie_dict['id'], writers_id=movie_dict['writers']))
        del movie_dict['writers']

        for key, value in movie_dict.copy().items():
            if value == 'N/A':
                del movie_dict[key]
            if key == 'imdb_rating' and key in movie_dict:
                movie_dict[key] = float(movie_dict.copy()[key])
            if key == 'plot' and key in movie_dict:
                movie_dict['description'] = movie_dict.pop('plot')
        movies.append(movie_dict)
    movie_actors1 = [imported_tables[3][key] for key in imported_tables[3]]
    movie_actors2 = [(item['movie_id'], item['actor_id']) for item in movie_actors1]
    movie_actors = defaultdict(list)
    for movie_id, actor_id in movie_actors2:
        movie_actors[movie_id].append(actor_id)
    movie_actors = list(movie_actors.items())


def load():
    for movie in movies:
        Movie(**movie).save()

    for actor in actors:
        Actor(**actor).save()

    for writer in writers:
        Writer(**writer).save()

    for movie_actor in movie_actors:
        actors_names = []
        actors_objs = []
        movie_obj = Movie.objects.get(pk=movie_actor[0])
        for id_actor in movie_actor[1]:
            actor_obj = Actor.objects.get(pk=id_actor)
            if actor_obj.name is not None:
                actors_names.append(actor_obj.name)
            actors_objs.append(actor_obj)
        if len(actors_names) > 0:
            movie_obj.actors_names = ', '.join(actors_names)
        movie_obj.save()
        movie_obj.actors.add(*actors_objs)

    for movie_writer in movie_writers:
        writers_names = []
        writers_objs = []
        movie_obj = Movie.objects.get(pk=movie_writer['movie_id'])
        for id_item in movie_writer['writers_id']:
            writer_obj = Writer.objects.get(pk=id_item)
            if writer_obj.name is not None:
                writers_names.append(writer_obj.name)
            writers_objs.append(writer_obj)
        if len(writers_names) > 0:
            movie_obj.writers_names = ', '.join(writers_names)
        movie_obj.save()
        movie_obj.writers.add(*writers_objs)


if __name__ == '__main__':
    extract()
    transform()
    load()
