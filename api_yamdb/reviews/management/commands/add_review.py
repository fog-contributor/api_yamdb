from django.core.management.base import BaseCommand

import csv

from reviews.models import Review, Title, User


class Command(BaseCommand):
    help = 'Добавляет review.csv в БД'

    def handle(self, *args, **options):
        with open('static/data/review.csv') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for row in reader:
                _, created = Review.objects.get_or_create(
                    id=row[0],
                    title=Title.objects.get(id=row[1]),
                    text=row[2],
                    author=User.objects.get(id=row[3]),
                    score=row[4],
                    pub_date=row[5]
                )
