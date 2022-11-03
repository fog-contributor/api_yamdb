from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

from reviews.domain import ADMIN, MODERATOR, ROLE, USER


class User(AbstractUser):
    """Расширенная пользовательская модель."""

    email = models.EmailField('Email', unique=True)
    bio = models.TextField('Биография', blank=True)
    otp = models.CharField(
        'Одноразовый пароль',
        blank=True,
        max_length=128
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=10,
        choices=ROLE,
        default=USER,
        help_text=(
            'Администратор, модератор или пользователь. По умолчанию user.'
        ),
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):

        return bool(self.role == ADMIN
                    or self.is_superuser)

    @property
    def is_moderator(self):

        return bool(self.role == MODERATOR
                    or self.is_superuser)


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Добавление жанра."""

    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения, к которым пишут отзывы (фильм, книга или песенка)."""

    name = models.CharField('Название', max_length=128)
    year = models.PositiveIntegerField('Год выпуска')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre')
    )
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Slug категории'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательная модель для связи m2m."""

    title = models.ForeignKey(
        'Title',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        null=True,
        related_name='genre_titles',
        verbose_name='Жанр'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Обзоры произведений."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к обзорам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='ID произведения'
    )
    text = models.TextField('Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='ID автора'
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
