import datetime as dt

from django.conf import settings
from django.db import models

from .constants import SYMBOLS_FOR_TEXT_FIELD
from .validators import validate_year, validate_score


class CategoryGenreBase(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(CategoryGenreBase):
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField("Слаг категории", unique=True)

    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):
    name = models.CharField("Название жанра", max_length=100)
    slug = models.SlugField("Слаг жанра", unique=True)

    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField("Название", max_length=100)
    year = models.PositiveSmallIntegerField(
        validators=[validate_year],
        verbose_name="Год выпуска",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория произведения",
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр произведения",
    )
    description = models.TextField("Описание произведения")

    class Meta:
        ordering = ["name"]
        default_related_name = "titles"

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    text = models.TextField("Текс отзыва")
    score = models.PositiveSmallIntegerField(
        validators=[validate_score],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Публикация"
    )

    class Meta:
        default_related_name = "reviews"
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:SYMBOLS_FOR_TEXT_FIELD]


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    text = models.TextField("Текс отзыва")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name="Отзыв"
    )

    class Meta:
        default_related_name = "comments"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:SYMBOLS_FOR_TEXT_FIELD]
