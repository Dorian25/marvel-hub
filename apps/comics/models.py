from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from datetime import datetime

class Series(models.Model, HitCountMixin):
    """
    DROP TABLE IF EXISTS series CASCADE;

    CREATE TABLE series (
    seriesID SERIAL PRIMARY KEY NOT NULL,
    rawname VARCHAR(255),
    cleanname VARCHAR(255),
    num VARCHAR(10),
    publicationdate VARCHAR(50),
    publisher VARCHAR(255),
    type VARCHAR(255),
    genre VARCHAR(255),
    status VARCHAR(255),
    logo TEXT,
    url_fandom TEXT);
    """
    series_id = models.AutoField(primary_key=True)
    rawname = models.CharField(max_length=255)
    cleanname = models.CharField(max_length=255)
    num = models.CharField(max_length=10)
    publicationdate = models.CharField(max_length=50)
    publisher = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    url_logo = models.TextField()
    url_fandom = models.TextField()

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

class Issue(models.Model, HitCountMixin):
    issue_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    release_date = models.DateField(default=datetime(1900,1,1))
    url_cover = models.TextField()
    url_read = models.TextField()
    
    # add _id by default for foreign key
    series = models.ForeignKey(Series, 
                               on_delete=models.CASCADE)
    
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )