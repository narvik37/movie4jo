from import_export import resources
from .models import Genre, Movie, Movie_Genre

class GenreResources(resources.ModelResources):
    class Meta:
        model = Genre

class MovieResources(resources.ModelResources):
    class Meta:
        model = Movie

class Movie_GenreResources(resources.ModelResources):
    class Meta:
        model = Movie_Genre