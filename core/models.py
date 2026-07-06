from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # e.g., 8.5

    # Images ke liye
    poster_image = models.ImageField(upload_to='movies/posters/')
    banner_image = models.ImageField(upload_to='movies/banners/', blank=True, null=True)

    genres = models.ManyToManyField(Genre)
    video_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title