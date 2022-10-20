from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField()


class Category(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True,)


class Title(models.Model):
    name = models.CharField()
    year = models.IntegerField()
    category = models.ForeignKey(Category,)


class Review(models.Model):
    SCORE_CHOICES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerChoices(choices=SCORE_CHOICES)
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


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
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
