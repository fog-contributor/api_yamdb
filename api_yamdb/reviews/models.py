from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):

    email = models.EmailField(unique=True)
    bio = models.TextField('Биография', blank=True, null=True)
    otp = models.CharField(null=True, blank=True, max_length=128)
    role = models.CharField(
        max_length=10,
        choices=ROLE,
        default='user',
        help_text=(
            'Администратор, модератор или пользователь. По умолчанию user.'
        ),
        blank=True)
