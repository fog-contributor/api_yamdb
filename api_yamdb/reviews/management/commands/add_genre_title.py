from django.core.management.base import BaseCommand

import csv

from reviews.models import Genre, GenreTitle, Title


class Command(BaseCommand):
    help = 'Добавляет genre_title.csv в БД'

    def handle(self, *args, **options):
        with open('static/data/genre_title.csv') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for row in reader:
                _, created = GenreTitle.objects.get_or_create(
                    id=row[0],
                    title=Title.objects.get(id=row[1]),
                    genre=Genre.objects.get(id=row[2])
                )
