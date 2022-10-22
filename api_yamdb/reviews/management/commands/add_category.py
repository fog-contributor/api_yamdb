from django.core.management.base import BaseCommand

import csv

from reviews.models import Category


class Command(BaseCommand):
    help = 'Добавляет category.csv в БД'

    def handle(self, *args, **options):
        with open('static/data/category.csv') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for row in reader:
                _, created = Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )
