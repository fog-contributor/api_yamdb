from django.core.management.base import BaseCommand

import csv

from reviews.models import Category, Title


class Command(BaseCommand):
    help = 'Добавляет titles.csv в БД'

    def handle(self, *args, **options):
        with open('static/data/titles.csv') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for row in reader:
                _, created = Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=Category.objects.get(id=row[3])
                )
