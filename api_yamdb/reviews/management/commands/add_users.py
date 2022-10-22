from django.core.management.base import BaseCommand

import csv

from reviews.models import User


class Command(BaseCommand):
    help = 'Добавляет users.csv в БД'

    def handle(self, *args, **options):
        with open('static/data/users.csv') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for row in reader:
                _, created = User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3]
                )
