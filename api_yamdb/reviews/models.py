from django.contrib.auth.models import AbstractUser
# from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)
SCORE_CHOICES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


class User(AbstractUser):
    """
    Кастомная модель user c уникальным username и email.
    """
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


class Category(models.Model):
    """
    Категории (типы) произведений.
    """
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return self.name

# class Comment(models.Model):
#     """"""
#     title = models.ForeignKey(
#         'Title',
#         on_delete=models.CASCADE,
#         related_name='comments',
#         verbose_name='ID произведения'
#     )
#     author = models.ForeignKey(
#         'User',
#         on_delete=models.CASCADE,
#         related_name='comments',
#         verbose_name='Автор'
#     )
#     text = models.TextField('Текст комментария')
#     pub_date = models.DateTimeField(
#         'Дата публикации',
#         auto_now_add=True,
#     )


class Genre(models.Model):
    """
    Добавление жанра.
    """
    name = models.CharField('Название жанра', max_length=128)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return self.name

# class Review(models.Model):
#     """
#     Добавить новый отзыв. Пользователь может оставить только один отзыв.
#     """
#     title_id = models.ForeignKey(
#         # 'ID произведения',
#         'Title',
#         on_delete=models.CASCADE,
#         related_name='reviews'
#     )
#     text = models.CharField('Текст отзыва', max_length=256)
#     score = models.IntegerField(
#         'Оценка от 1 до 10',
#         validators=[MinValueValidator(1), MaxValueValidator(10)],
#         # choices=SCORE_CHOICES
#     )


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
    """
    name = models.CharField('Название', max_length=128)
    year = models.DateTimeField('Год выпуска')
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Slug жанра'

    )
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Slug категории'
    )
