from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount

# Create your models here.
class Movie(models.Model, HitCountMixin):
    movie_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url_cover = models.TextField()
    release_date = models.DateField()
    url_watch = models.TextField()

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )