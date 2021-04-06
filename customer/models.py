from django.db import models
from django import forms

# Create your models here.

class Genre(models.Model):
    genreId = models.AutoField(primary_key=True)
    genreName = models.CharField(max_length=16, verbose_name="genre_name")

    created = models.DateTimeField(auto_now_add=True, verbose_name="register_time")
    update = models.DateTimeField(auto_now_add=True, verbose_name="modify_time")

    class Meta:
        db_table = "genre"
        verbose_name = "Genre"
        verbose_name_plural = "Genre"
        
    def __str__(self):
        return self.genreName

class Movie(models.Model):
    movieId = models.CharField(max_length=16, verbose_name="movie_id", primary_key=True)
    movieName = models.CharField(max_length=16, verbose_name="movie_name")
    year = models.CharField(max_length=16, verbose_name="year")
    director = models.CharField(max_length=16, verbose_name="director")
    actor = models.CharField(max_length=128, verbose_name="actor")
    plot = models.CharField(max_length=512, verbose_name="plot")
    rate = models.CharField(max_length=8, verbose_name="rate", default='')
    image = models.ImageField(upload_to='movie/', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name="register_time")
    update = models.DateTimeField(auto_now_add=True, verbose_name="modify_time")

    class Meta:
        db_table = "movie"
        verbose_name = "Movie"
        verbose_name_plural = "Movie"
        
    def __str__(self):
        return self.movieName

class Movie_Genre(models.Model):
    movieId = models.ForeignKey("Movie", verbose_name="movie_id", on_delete=models.CASCADE, db_column="movie_id")
    genreId = models.ForeignKey("Genre", verbose_name="genre_id", on_delete=models.CASCADE, db_column="genre_id")

    created = models.DateTimeField(auto_now_add=True, verbose_name="register_time")
    update = models.DateTimeField(auto_now_add=True, verbose_name="modify_time")

    class Meta:
        db_table = "movie_genre"
        verbose_name = "Movie_Genre"
        verbose_name_plural = "Movie_Genre"
        
    def __str__(self):
        return self.genreName