from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE = (('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор'))


class User(AbstractUser):
    # password = None
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': ("A user with that email already exists."),
        },
    )
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE,
        default='user',
        help_text=(
            'Администратор, модератор или пользователь. По умолчанию user.'
        ),
        blank=True
    )
