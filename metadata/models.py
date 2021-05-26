from django.db import models

# Create your models here.

class Genre(models.Model):
    id = models.CharField(max_length=16, verbose_name="genre_id", primary_key=True, default='')
    genre_name = models.CharField(max_length=32, verbose_name="genre_name", default='')

    created = models.DateTimeField(auto_now_add=True, verbose_name="register_time", null=True)
    update = models.DateTimeField(auto_now_add=True, verbose_name="modify_time")

    class Meta:
        db_table = "genre"
        verbose_name = "Genre"
        verbose_name_plural = "Genre"
        
    def __str__(self):
        return self.genre_name

class Movie(models.Model):
    id = models.CharField(max_length=16, verbose_name="movie_id", primary_key=True)
    title = models.CharField(max_length=128, verbose_name="movie_title", default='')
    imdb_id = models.CharField(max_length=16, verbose_name="imdb_id", default='')
    release_date = models.CharField(max_length=16, verbose_name="release_date", default='')
    vote_average = models.CharField(max_length=8, verbose_name="vote_average", default='')
    overview = models.CharField(max_length=1024, verbose_name="overview", default='')
    poster_url = models.CharField(max_length=256, verbose_name="poster_url", default='')
    director = models.CharField(max_length=64, verbose_name="director", default='')
    main_actor = models.CharField(max_length=64, verbose_name="main_actor", default='')
    # image = models.ImageField(upload_to='movie/', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name="register_time")
    update = models.DateTimeField(auto_now_add=True, verbose_name="modify_time")

    class Meta:
        db_table = "movie"
        verbose_name = "Movie"
        verbose_name_plural = "Movie"
        
    def __str__(self):
        return self.title

class Movie_Genre(models.Model):
    movie_id = models.CharField(max_length=16, verbose_name="movie_id", default='')
    genre_id = models.CharField(max_length=16, verbose_name="genre_id", default='')

    created = models.DateTimeField(auto_now_add=True, verbose_name="register_time")
    update = models.DateTimeField(auto_now_add=True, verbose_name="modify_time")

    class Meta:
        db_table = "movie_genre"
        verbose_name = "Movie_Genre"
        verbose_name_plural = "Movie_Genre"
        
    def __str__(self):
        return self.movie_id

class First_Genre(models.Model):
    movie_id = models.CharField(max_length=16, verbose_name="movie_id", default='')
    genre_id = models.CharField(max_length=16, verbose_name="genre_id", default='')

    created = models.DateTimeField(auto_now_add=True, verbose_name="register_time")
    update = models.DateTimeField(auto_now_add=True, verbose_name="modify_time")

    class Meta:
        db_table = "first_genre"
        verbose_name = "First_Genre"
        verbose_name_plural = "First_Genre"
        
    def __str__(self):
        return self.movie_id