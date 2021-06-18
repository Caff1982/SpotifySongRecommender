# Generated by Django 3.2.4 on 2021-06-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_id', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=500)),
                ('artist', models.CharField(max_length=800)),
                ('artist_id', models.CharField(max_length=1000)),
                ('popularity', models.IntegerField()),
                ('duration_ms', models.IntegerField()),
                ('is_explicit', models.BooleanField(default=False)),
                ('release_year', models.IntegerField()),
                ('danceability', models.FloatField()),
                ('energy', models.FloatField()),
                ('key', models.IntegerField()),
                ('loudness', models.FloatField()),
                ('is_major', models.BooleanField(default=True)),
                ('speechiness', models.FloatField()),
                ('acousticness', models.FloatField()),
                ('instrumentalness', models.FloatField()),
                ('liveness', models.FloatField()),
                ('valence', models.FloatField()),
                ('tempo', models.FloatField()),
                ('time_signature', models.IntegerField()),
            ],
        ),
    ]
