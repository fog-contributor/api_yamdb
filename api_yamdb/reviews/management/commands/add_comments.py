from django.core.management.base import BaseCommand

import csv

from reviews.models import Comment, Review, User


class Command(BaseCommand):
    help = 'Добавляет comments.csv в БД'

    def handle(self, *args, **options):
        with open('static/data/comments.csv') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for row in reader:
                _, created = Comment.objects.get_or_create(
                    id=row[0],
                    review=Review.objects.get(id=row[1]),
                    text=row[2],
                    author=User.objects.get(id=row[3]),
                    pub_date=row[4]
                )
