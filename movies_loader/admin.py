from django.contrib import admin

from .models import Actor, Writer, Movie

admin.site.register(Actor)
admin.site.register(Writer)
admin.site.register(Movie)

