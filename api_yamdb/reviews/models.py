from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):

    name = models.CharField('Имя роли', max_length=50)
    description = models.TextField('Описание ролевой модели')

    def __str__(self):
        return self.name


class User(AbstractUser):

    role = models.ForeignKey(Role,
                             on_delete=models.CASCADE,
                             related_name='role',
                             blank=True, null=True)

    bio = models.TextField('Биография', blank=True, null=True)
