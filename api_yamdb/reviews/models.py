from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg


ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    """
    Расширенная пользовательская модель.
    """
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


class Category(models.Model):
    """
    Категории (типы) произведений.
    """
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """
    Добавление жанра.
    """
    name = models.CharField('Название жанра', max_length=128)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или
    песенка).
    """
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

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.reviews.aggregate(Avg('score'))

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    """Вспомогательная модель для связи m2m."""
    title = models.ForeignKey(
        'Title',
        on_delete=models.SET_NULL,
        null=True,
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
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            ),
        ]


class Comment(models.Model):
    """Комментарии к обзорам."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("-pub_date",)
