# Generated by Django 4.2.6 on 2023-11-13 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('character_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Reality',
            fields=[
                ('reality_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=25)),
                ('current_alias', models.CharField(max_length=25)),
                ('aliases', models.TextField()),
                ('url_logo', models.TextField()),
                ('url_fandom', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('version_id', models.AutoField(primary_key=True, serialize=False)),
                ('current_alias', models.CharField(max_length=255)),
                ('image', models.TextField()),
                ('gender', models.CharField(max_length=25)),
                ('eyes', models.CharField(max_length=25)),
                ('hair', models.CharField(max_length=25)),
                ('origin', models.CharField(max_length=25)),
                ('living_status', models.CharField(max_length=25)),
                ('intelligence_power', models.IntegerField()),
                ('strength_power', models.IntegerField()),
                ('speed_power', models.IntegerField()),
                ('durability_power', models.IntegerField()),
                ('energy_projection_power', models.IntegerField()),
                ('fighting_skills_power', models.IntegerField()),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.character')),
                ('reality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.reality')),
            ],
        ),
    ]