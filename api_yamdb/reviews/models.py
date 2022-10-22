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


class Comment(models.Model):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ("-pub_date",)


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


class Review(models.Model):
    SCORE_CHOICES = ((1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10))

    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            ),
        ]


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    '''Вспомогательная модель для связи m2m.'''
    title = models.ForeignKey(
        'Title',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        null=True,
        related_name='genry_titles',
        verbose_name='Жанр'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'
