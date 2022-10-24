from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'Добавляет csv файлов в БД'

    def handle(self, *args, **options):
        management.call_command('add_category')
        print('Категории успешно добавлены в БД')
        management.call_command('add_genre')
        print('Жанры успешно добавлены в БД')
        management.call_command('add_titles')
        print('Произведения успешно добавлены в БД')
        management.call_command('add_users')
        print('Пользователи успешно добавлены в БД')
        management.call_command('add_review')
        print('Отзывы успешно добавлены в БД')
        management.call_command('add_genre_title')
        print('genre_title успешно добавлены в БД')
        management.call_command('add_comments')
        print('Коментарии успешно добавлены в БД')
