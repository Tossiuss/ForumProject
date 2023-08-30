from django.db import models
from django.contrib.auth import get_user_model
from apps.publication.models import Posts

# Create your models here.

User = get_user_model()

class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.name} -> {self.post.title}'


class Like(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Пользователь'
    )
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Пост'
    )

    def __str__(self):
        return f'Liked by {self.author.name}'

class Rating(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='Пользователь'
    )
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='Пост'
    )
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.rating} -> {self.post.title}'
