from django.db import models


class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Имя актера', null=True)

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'

    def __str__(self):
        name = self.name
        if name is None:
            name = 'Empty'
        return name


class Writer(models.Model):
    id = models.CharField(max_length=27, primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Имя сценариста', null=True)

    class Meta:
        verbose_name = 'Сценарист'
        verbose_name_plural = 'Сценаристы'

    def __str__(self):
        name = self.name
        if name is None:
            name = 'Empty'
        return name


class Movie(models.Model):
    id = models.CharField(max_length=9, primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Название фильма', null=True)
    imdb_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    genre = models.CharField(max_length=255, verbose_name='Жанр', null=True)
    description = models.TextField(verbose_name='Описание фильма', null=True)
    writers = models.ManyToManyField(Writer, verbose_name='Сценаристы', related_name='movie_writers')
    writers_names = models.TextField(verbose_name='Имена сценаристов', null=True)
    director = models.CharField(max_length=255, verbose_name='Режисер', null=True)
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='movie_actors')
    actors_names = models.TextField(verbose_name='Имена актеров', null=True)

    class Meta:
        verbose_name = 'Фильм '
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title
