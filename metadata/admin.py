from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import Genre, Movie, Movie_Genre, First_Genre

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

# Register your models here.

@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'release_date', 'poster_url', 'director', 'main_actor']
    search_fields = ['title', 'id']
    pass

@admin.register(Genre)
class MovieAdmin(ImportExportModelAdmin):
    list_display = ['id', 'genre_name']
    search_fields = ['genre_name']
    pass

@admin.register(Movie_Genre)
class MovieAdmin(ImportExportModelAdmin):
    list_display = ['movie_id', 'genre_id']
    search_fields = ['movie_id']
    pass

@admin.register(First_Genre)
class MovieAdmin(ImportExportModelAdmin):
    list_display = ['movie_id', 'genre_id']
    search_fields = ['movie_id']
    pass