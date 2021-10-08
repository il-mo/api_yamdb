from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Titles(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.text


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.PositiveIntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    reviews = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категоря'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
