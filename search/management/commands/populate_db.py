import csv
import re
from tqdm import tqdm

from django.core.management.base import BaseCommand

from search.models import Song


class Command(BaseCommand):
    help = 'Updates database from csv file'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        """
        Iterates through rows in csv and creates Song objects.
        """
        with open(options['filepath'], 'r') as f:
            reader = csv.DictReader(f)
            for line in tqdm(reader):
                # Remove special characters from string
                artist = re.sub('[^A-Za-z0-9 ]+', '', line['artists'])
                is_explicit = line['explicit'] == '1'
                year = line['release_date'].split('-')[0]
                is_major = line['mode'] == '1'

                Song.objects.get_or_create(
                    song_id=line['id'], name=line['name'], artist=artist,
                    popularity=line['popularity'],
                    duration_ms=line['duration_ms'], is_explicit=is_explicit,
                    release_year=year, danceability=line['danceability'],
                    energy=line['energy'], key=line['key'],
                    loudness=line['loudness'], is_major=is_major,
                    speechiness=line['speechiness'],
                    acousticness=line['acousticness'],
                    instrumentalness=line['instrumentalness'],
                    liveness=line['liveness'], valence=line['valence'],
                    tempo=line['tempo'], time_signature=line['time_signature']
                    )
