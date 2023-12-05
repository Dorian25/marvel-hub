from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount

# Create your models here.

class Reality(models.Model):
    reality_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    status = models.CharField(max_length=25)
    current_alias = models.CharField(max_length=25)
    aliases = models.TextField()
    url_logo = models.TextField()
    url_fandom = models.TextField()

    def __str__(self):
        return self.name

class Character(models.Model, HitCountMixin):
    character_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    
    def __str__(self):
        return self.name

class Version(models.Model):
    version_id = models.AutoField(primary_key=True)

    # add _id by default for foreign key
    character = models.ForeignKey(Character, 
                                on_delete=models.CASCADE)

    url_fandom = models.TextField()
    url_image = models.TextField()

    name_primary = models.CharField(max_length=255)
    name_secondary = models.CharField(max_length=255)
    current_alias = models.CharField(max_length=255)
    
    # physical characteristics
    gender = models.CharField(max_length=25)
    eyes = models.CharField(max_length=25)
    hair = models.CharField(max_length=25)
    skin = models.CharField(max_length=25)


    # origin & living status
    origin = models.CharField(max_length=25)
    living_status = models.CharField(max_length=25)
    ## add _id by default for foreign key
    reality = models.ForeignKey(Reality, 
                               on_delete=models.CASCADE)

    # personal information

    # power
    intelligence_power = models.IntegerField(default=0)
    strength_power = models.IntegerField(default=0)
    speed_power = models.IntegerField(default=0)
    durability_power = models.IntegerField(default=0)
    energy_projection_power = models.IntegerField(default=0)
    fighting_skills_power = models.IntegerField(default=0)