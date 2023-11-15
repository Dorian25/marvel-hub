from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url_cover = models.TextField()
    release_date = models.DateField()
    url_watch = models.TextField()

    def __str__(self):
        return self.name