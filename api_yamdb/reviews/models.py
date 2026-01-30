import datetime as dt
from .constants import SYMBOLS_FOR_TEXT_FIELD
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


User = get_user_model()


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError('Нельзя добавлять произведения будущего!')


def validate_score(value):
    if value < 1 or value > 10:
        raise ValidationError('Оценка должна быть от 1 до 10')


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField('Слаг категории', unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=100)
    slug = models.SlugField('Слаг жанра', unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=100)
    year = models.PositiveSmallIntegerField(
        validators=[validate_year],
        verbose_name='Год выпуска',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
    )
    description = models.TextField('Описание произведения')

    class Meta:
        ordering = ['name']
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Текс отзыва')
    score = models.PositiveSmallIntegerField(
        validators=[validate_score],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:SYMBOLS_FOR_TEXT_FIELD]
    

class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Текс отзыва')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:SYMBOLS_FOR_TEXT_FIELD]