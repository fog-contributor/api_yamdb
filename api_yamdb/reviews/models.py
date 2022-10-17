from django.db import models

SCORE_CHOICES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    score = models.IntegerChoices(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text


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
